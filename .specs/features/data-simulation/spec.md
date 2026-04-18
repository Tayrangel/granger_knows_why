# Data Simulation & Ingestion — Specification

## Problem Statement

O sistema precisa de dados financeiros simulados com erros intencionais controlados para que o agente tenha cenários reais para questionar. Sem dados com inconsistências plausíveis (status conflitantes, duplicidades, cancelamentos parciais), o agente não consegue demonstrar valor.

## Goals

- [ ] Gerar ~3.700 registros distribuídos em 3 fontes com erros intencionais rastreáveis
- [ ] Carregar todos os dados no PostgreSQL (`granger_db`) de forma idempotente

## Out of Scope

| Feature | Reason |
| --- | --- |
| Dados reais de sistemas financeiros | MVP usa apenas dados fictícios |
| Streaming ou ingestão incremental | Carga batch única é suficiente |
| Validação de schema no load | A validação acontece na camada dbt |

---

## User Stories

### P1: Gerar dados bancários com erros intencionais ⭐ MVP

**User Story:** Como desenvolvedor do sistema, quero um script que gere ~1.000 registros de `bank_transactions` com erros intencionais controlados para que o agente tenha material para questionar.

**Why P1:** Sem dados bancários, não há saldo diário, nem demonstração de transações pendentes distorcendo receita.

**Acceptance Criteria:**

1. WHEN o script é executado THEN system SHALL gerar exatamente ~1.000 registros em `bank_transactions`
2. WHEN os dados são gerados THEN system SHALL incluir os campos: `transaction_id` (UUID único), `amount`, `payment_method` (`credit`/`debit`), `balance_after`, `event_date`, `processing_date`, `status`
3. WHEN os dados são gerados THEN system SHALL inserir ~5% de registros com `status = 'pending'` mas `balance_after` calculado como `processed`
4. WHEN os dados são gerados THEN system SHALL inserir ~3% de registros duplicados (mesmo `amount` + `event_date`, `transaction_id` diferente)

**Independent Test:** Executar `SELECT COUNT(*), status FROM bank_transactions GROUP BY status` e verificar a presença de `pending` com proporção esperada.

---

### P1: Gerar dados de cartão com erros intencionais ⭐ MVP

**User Story:** Como desenvolvedor, quero ~1.500 registros de `card_transactions` com autorizações sem captura e cancelamentos inconsistentes.

**Why P1:** O cenário de "TPV com duplicidade" — um dos 3 obrigatórios do PRD — depende de auth + capture sem filtro.

**Acceptance Criteria:**

1. WHEN o script é executado THEN system SHALL gerar ~1.500 registros com campos: `transaction_id`, `authorization_id`, `amount`, `captured_amount`, `event_type` (`authorization`/`capture`/`cancellation`), `status`, `event_date`
2. WHEN os dados são gerados THEN system SHALL incluir autorizações (`event_type = 'authorization'`) sem captura correspondente
3. WHEN os dados são gerados THEN system SHALL incluir cancelamentos parciais (`captured_amount != amount` original)
4. WHEN os dados são gerados THEN system SHALL incluir registros com `status = 'approved'` que possuem cancelamento posterior

**Independent Test:** `SELECT event_type, COUNT(*) FROM card_transactions GROUP BY event_type` — deve mostrar os 3 tipos presentes.

---

### P1: Gerar dados de adquirência com erros intencionais ⭐ MVP

**User Story:** Como desenvolvedor, quero ~1.200 registros de `acquirer_transactions` com `amount_net` calculado incorretamente em alguns casos.

**Why P1:** Suporta o cenário de "taxa ignorando cancelamentos" e "receita líquida distorcida".

**Acceptance Criteria:**

1. WHEN o script é executado THEN system SHALL gerar ~1.200 registros com campos: `transaction_id`, `card_transaction_id` (FK para `card_transactions`), `amount_gross`, `fee_amount`, `amount_net`, `settlement_date`, `status`
2. WHEN os dados são gerados THEN system SHALL calcular `amount_net` incorretamente em ~8% dos registros (ex: não subtrair fee)
3. WHEN os dados são gerados THEN system SHALL deixar `settlement_date` nulo para transações com `status = 'pending'`

**Independent Test:** `SELECT COUNT(*) FROM acquirer_transactions WHERE settlement_date IS NULL` — deve retornar valor > 0.

---

### P1: Carregar dados no PostgreSQL ⭐ MVP

**User Story:** Como desenvolvedor, quero um script `load_all.py` que carregue todos os dados gerados no banco `granger_db` de forma idempotente.

**Why P1:** Pré-requisito para todas as camadas dbt.

**Acceptance Criteria:**

1. WHEN `load_all.py` é executado THEN system SHALL criar as 3 tabelas se não existirem
2. WHEN `load_all.py` é executado novamente THEN system SHALL truncar e recarregar (idempotente)
3. WHEN a carga termina THEN system SHALL exibir contagem de registros por tabela

**Independent Test:** Executar `load_all.py` duas vezes e verificar que a contagem final é a mesma.

---

## Edge Cases

- WHEN o banco não está disponível THEN system SHALL falhar com mensagem de erro clara (não silencioso)
- WHEN `card_transaction_id` em `acquirer_transactions` não encontra par em `card_transactions` THEN system SHALL usar UUID válido de `card_transactions` existente

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| DATA-01 | P1: Gerar bank_transactions | Tasks | Pending |
| DATA-02 | P1: Gerar card_transactions | Tasks | Pending |
| DATA-03 | P1: Gerar acquirer_transactions | Tasks | Pending |
| DATA-04 | P1: Carregar no PostgreSQL | Tasks | Pending |

---

## Success Criteria

- [ ] `SELECT COUNT(*) FROM bank_transactions` retorna ~1.000
- [ ] `SELECT COUNT(*) FROM card_transactions` retorna ~1.500
- [ ] `SELECT COUNT(*) FROM acquirer_transactions` retorna ~1.200
- [ ] Erros intencionais estão presentes e rastreáveis via query
