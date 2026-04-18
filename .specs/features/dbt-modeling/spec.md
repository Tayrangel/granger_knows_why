# dbt Modeling (Bronze → Silver → Gold) — Specification

## Problem Statement

Os dados brutos carregados no PostgreSQL precisam ser transformados em modelos analíticos confiáveis, documentados e testados. Sem essa camada, o agente não tem contexto sobre a qualidade dos dados e as métricas não podem ser calculadas de forma rastreável.

## Goals

- [ ] Pipeline dbt executando sem erros do Bronze ao Gold
- [ ] Cada modelo SQL tem contrato de dados (`.yml`) com `data_tests`
- [ ] `fct_financial_transactions` e `fct_revenue` produzem métricas com armadilhas documentadas

## Out of Scope

| Feature | Reason |
| --- | --- |
| dbt Cloud ou CI/CD automático | MVP roda localmente |
| Snapshots ou modelos incrementais | Carga batch estática é suficiente |
| Exposures ou metrics YAML (dbt semantic layer) | Fora do escopo do MVP |

---

## User Stories

### P1: Bronze — Staging das 3 fontes ⭐ MVP

**User Story:** Como analytics engineer, quero modelos Bronze que limpem e tipem os dados brutos sem aplicar lógica de negócio, para que as camadas superiores partam de uma base confiável.

**Why P1:** Base de toda a modelagem. Sem Bronze, Silver e Gold não existem.

**Acceptance Criteria:**

1. WHEN `dbt run --select bronze` é executado THEN system SHALL criar `stg_bank_transactions`, `stg_card_transactions`, `stg_acquirer_transactions` sem erros
2. WHEN os modelos Bronze são criados THEN system SHALL aplicar cast de tipos, renomear colunas para snake_case e normalizar valores de enum para minúsculas
3. WHEN `dbt test --select bronze` é executado THEN system SHALL executar `not_null`, `unique` em `transaction_id` e `accepted_values` nos campos de enum — todos devem passar
4. WHEN `stg_acquirer_transactions` é criado THEN system SHALL incluir flag `has_settlement_discrepancy` (boolean) para registros com `amount_net` calculado incorretamente

**Independent Test:** `dbt build --select bronze` — zero falhas.

---

### P1: Silver — Modelo unificado de eventos financeiros ⭐ MVP

**User Story:** Como analytics engineer, quero um modelo Silver `int_financial_events` que una as 3 fontes em um único modelo de eventos financeiros normalizado.

**Why P1:** Pré-requisito direto para `fct_financial_transactions` no Gold.

**Acceptance Criteria:**

1. WHEN `dbt run --select silver` é executado THEN system SHALL criar `int_financial_events` sem erros
2. WHEN `int_financial_events` é criado THEN system SHALL conter os campos: `transaction_id`, `source` (`bank`/`card`/`acquirer`), `amount_gross`, `amount_net`, `event_date`, `settlement_date`, `status`, `is_settled` (boolean), `is_duplicate` (boolean)
3. WHEN `dbt test --select silver` é executado THEN system SHALL executar `not_null` em `transaction_id` e `source` — todos devem passar

**Independent Test:** `SELECT source, COUNT(*) FROM int_financial_events GROUP BY source` — deve mostrar os 3 valores.

---

### P1: Gold — Tabela fato e métricas com armadilhas ⭐ MVP

**User Story:** Como analytics engineer, quero modelos Gold `fct_financial_transactions` e `fct_revenue` que exponham métricas calculadas com armadilhas intencionais documentadas no `.yml`.

**Why P1:** É o que o agente consome como contexto analítico. Sem Gold, o agente não tem dados.

**Acceptance Criteria:**

1. WHEN `dbt run --select gold` é executado THEN system SHALL criar `fct_financial_transactions` e `fct_revenue` sem erros
2. WHEN `fct_revenue` é criado THEN system SHALL calcular: `gross_revenue` (inclui não liquidadas), `net_revenue`, `tpv` (pode ter duplicidade), `acquirer_fee_rate`, `daily_balance`
3. WHEN `dbt test --select gold` é executado THEN system SHALL validar `not_null` em todas as métricas e `net_revenue <= gross_revenue`
4. WHEN o `.yml` do Gold é lido THEN system SHALL conter descrição de cada métrica com nota sobre sua armadilha associada

**Independent Test:** `SELECT gross_revenue, net_revenue FROM fct_revenue LIMIT 5` — `net_revenue` deve ser ≤ `gross_revenue` em todos os registros.

---

### P2: Testes dbt customizados

**User Story:** Como analytics engineer, quero testes genéricos customizados que validem cenários específicos de qualidade dos dados além dos testes built-in do dbt.

**Why P2:** Aumenta confiança no pipeline; os erros intencionais devem ser rastreáveis, não ocultos.

**Acceptance Criteria:**

1. WHEN `assert_no_duplicate_transactions` é executado THEN system SHALL retornar zero linhas (duplicatas são rastreadas via flag `is_duplicate`, não removidas)
2. WHEN `assert_settled_amounts_non_negative` é executado THEN system SHALL retornar zero linhas com `amount_net < 0` em registros com `is_settled = true`

**Independent Test:** `dbt test --select tag:custom` — zero falhas.

---

## Edge Cases

- WHEN uma tabela raw está vazia THEN system SHALL o modelo Bronze retornar 0 linhas sem erro (não falhar o pipeline)
- WHEN `card_transaction_id` em `acquirer_transactions` não existe em `stg_card_transactions` THEN system SHALL o teste `relationships` falhar e reportar os IDs problemáticos

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| DBT-01 | P1: Bronze staging | Tasks | Pending |
| DBT-02 | P1: Silver int_financial_events | Tasks | Pending |
| DBT-03 | P1: Gold fct_financial_transactions | Tasks | Pending |
| DBT-04 | P1: Gold fct_revenue com armadilhas | Tasks | Pending |
| DBT-05 | P2: Testes customizados | Tasks | Pending |

---

## Success Criteria

- [ ] `dbt build` (run + test) completo sem erros em todas as camadas
- [ ] Todos os modelos têm `.yml` com `data_tests` e descrição de colunas
- [ ] `fct_revenue` expõe as 5 métricas com armadilhas documentadas
- [ ] Testes customizados passam sem erros
