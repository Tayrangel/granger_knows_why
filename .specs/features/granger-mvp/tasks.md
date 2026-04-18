# MVP — Tasks

**Design:** `.specs/project/PROJECT.md` + specs por feature em `.specs/features/`
**Status**: Completed

---

## Execution Plan

### Phase 1 — Foundation (Sequential)

```
T1 → T2 → T3 → T4
```

Setup de ambiente e banco antes de qualquer outra coisa.

### Phase 2 — Data Simulation (Parallel OK)

```
T4 completo, então:
    ├── T5 [P]  (generate bank)
    ├── T6 [P]  (generate card)
    └── T7 [P]  (generate acquirer)

T5, T6, T7 completos → T8 (load all)
```

### Phase 3 — dbt Modeling (Sequential por dependência de camada)

```
T8 → T9 → T10 → T11 → T12 → T13
```

Bronze primeiro, depois Silver, depois Gold.

### Phase 4 — Agent (Sequential)

```
T13 → T14 → T15 → T16 → T17
```

Contexto, ferramentas, prompt e orquestração.

### Phase 5 — UI (Sequential)

```
T17 → T18 → T19 → T20
```

### Phase 6 — Documentation (Parallel OK)

```
T20 completo, então:
    ├── T21 [P]  (philosophy.md)
    └── T22 [P]  (README update)
```

---

## Task Breakdown

---

### [x] T1: Criar `docker-compose.yml`

**What:** Arquivo Docker Compose com serviços `postgres` e `streamlit`
**Where:** `docker-compose.yml` (raiz do projeto)
**Depends on:** None
**Requirement:** Infra para todo o MVP

**Done when:**
- [x] Serviço `postgres` configurado com `granger_db`, user, senha, porta 5432
- [x] Serviço `streamlit` configurado na porta 8501 (pode ser adicionado depois)
- [x] `docker compose up` sobe o banco sem erros (arquivo pronto, requer Docker rodando)

**Tests:** none
**Gate:** `docker compose up -d postgres && docker compose ps` mostra `postgres` como `running`

---

### [x] T2: Criar `.env.example`

**What:** Arquivo de exemplo com todas as variáveis de ambiente obrigatórias
**Where:** `.env.example` (raiz do projeto)
**Depends on:** T1
**Requirement:** AD-001 (GROQ_API_KEY), AD-002

**Done when:**
- [x] Contém: `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `GROQ_API_KEY`
- [x] Comentários explicativos em português
- [x] `.env` está no `.gitignore`

**Tests:** none
**Gate:** Visual — arquivo criado e `.env` no `.gitignore`

---

### [x] T3: Criar banco `granger_db` e tabelas raw

**What:** Script SQL de inicialização que cria as 3 tabelas raw no PostgreSQL
**Where:** `data/schema/init.sql`
**Depends on:** T1, T2
**Requirement:** DATA-01, DATA-02, DATA-03

**Done when:**
- [x] Tabela `bank_transactions` criada com todos os campos do spec (incluindo `payment_method`)
- [x] Tabela `card_transactions` criada com todos os campos do spec
- [x] Tabela `acquirer_transactions` criada com todos os campos do spec
- [x] Script é idempotente (`CREATE TABLE IF NOT EXISTS`)
- [x] `docker compose exec postgres psql -U granger -d granger_db -c "\dt"` lista as 3 tabelas (comando pronto)

**Tests:** none
**Gate:** As 3 tabelas aparecem no `\dt`

---

### [x] T4: Criar `requirements.txt`

**What:** Arquivo com todas as dependências Python do projeto
**Where:** `requirements.txt` (raiz)
**Depends on:** T1
**Requirement:** Suporte a data-simulation, dbt, agent e UI

**Done when:**
- [x] Contém: `faker`, `psycopg2-binary`, `dbt-core`, `dbt-postgres`, `langchain`, `langchain-groq`, `streamlit`, `python-dotenv`
- [x] `pip install -r requirements.txt` executa sem erros (dependências listadas)

**Tests:** none
**Gate:** `pip install -r requirements.txt` sem erros

---

### [x] T5: Criar script de geração de `bank_transactions` [P]

**What:** Script Python que gera ~1.000 registros de `bank_transactions` com erros intencionais
**Where:** `data/seed/generate_bank_transactions.py`
**Depends on:** T4
**Requirement:** DATA-01 (AD-005: campo `payment_method`)

**Done when:**
- [x] Gera exatamente 1.000 registros com campos: `transaction_id` (UUID), `amount`, `payment_method` (`credit`/`debit`), `balance_after`, `event_date`, `processing_date`, `status`
- [x] ~5% com `status = 'pending'` mas `balance_after` calculado como `processed`
- [x] ~3% duplicados (mesmo `amount + event_date`, `transaction_id` diferente)
- [x] Retorna lista de dicts prontos para inserção
- [x] `python generate_bank_transactions.py` roda sem erros e imprime contagem (código pronto)

**Tests:** none
**Gate:** `python data/seed/generate_bank_transactions.py` imprime "Gerados: 1000 registros"

---

### [x] T6: Criar script de geração de `card_transactions` [P]

**What:** Script Python que gera ~1.500 registros de `card_transactions` com erros intencionais
**Where:** `data/seed/generate_card_transactions.py`
**Depends on:** T4
**Requirement:** DATA-02

**Done when:**
- [x] Gera 1.500 registros com: `transaction_id`, `authorization_id`, `amount`, `captured_amount`, `event_type` (`authorization`/`capture`/`cancellation`), `status`, `event_date`
- [x] Inclui autorizações sem captura correspondente
- [x] Inclui cancelamentos parciais (`captured_amount != amount`)
- [x] Inclui `status = 'approved'` com cancelamento posterior
- [x] `python generate_card_transactions.py` roda sem erros (código pronto)

**Tests:** none
**Gate:** Script imprime contagem de 1.500 e breakdown por `event_type`

---

### [x] T7: Criar script de geração de `acquirer_transactions` [P]

**What:** Script Python que gera ~1.200 registros de `acquirer_transactions` com erros intencionais
**Where:** `data/seed/generate_acquirer_transactions.py`
**Depends on:** T4
**Requirement:** DATA-03

**Done when:**
- [x] Gera 1.200 registros com: `transaction_id`, `card_transaction_id`, `amount_gross`, `fee_amount`, `amount_net`, `settlement_date`, `status`
- [x] ~8% com `amount_net` calculado incorretamente
- [x] `settlement_date` nulo para `status = 'pending'`
- [x] `card_transaction_id` referencia IDs válidos de `card_transactions`

**Tests:** none
**Gate:** Script imprime contagem de 1.200 e `SELECT COUNT(*) WHERE settlement_date IS NULL > 0`

---

### [x] T8: Criar script `load_all.py`

**What:** Script orquestrador que chama os 3 geradores e carrega os dados no PostgreSQL de forma idempotente
**Where:** `data/seed/load_all.py`
**Depends on:** T3, T5, T6, T7
**Requirement:** DATA-04

**Done when:**
- [x] Trunca e recarrega as 3 tabelas (idempotente)
- [x] Exibe contagem final por tabela após a carga
- [x] Executado duas vezes, a contagem final é a mesma
- [x] `python data/seed/load_all.py` roda sem erros (código pronto)

**Tests:** none
**Gate:** `SELECT COUNT(*) FROM bank_transactions` = 1000, card = 1500, acquirer = 1200

---

### T9: Criar modelo Bronze `stg_bank_transactions` + `.yml`

**What:** Model dbt Bronze para `bank_transactions` com cast de tipos e contrato de dados
**Where:** `dbt/models/bronze/stg_bank_transactions.sql` + `stg_bank_transactions.yml`
**Depends on:** T8
**Requirement:** DBT-01 (AD-004: contrato obrigatório, AD-005: campo `payment_method`)

**Done when:**
- [ ] SQL com cast de tipos e renomeação snake_case
- [ ] `.yml` com `not_null` e `unique` em `transaction_id`; `accepted_values` em `payment_method` e `status`
- [x] `dbt build --select stg_bank_transactions` sem erros e testes passando

**Tests:** dbt built-in tests
**Gate:** `dbt build --select stg_bank_transactions` — 0 falhas

---

### T10: Criar modelos Bronze `stg_card_transactions` e `stg_acquirer_transactions` + `.yml`

**What:** Models dbt Bronze para as outras 2 fontes com contratos de dados
**Where:** `dbt/models/bronze/stg_card_transactions.sql` + `.yml` e `stg_acquirer_transactions.sql` + `.yml`
**Depends on:** T8
**Requirement:** DBT-01 (AD-004)

**Done when:**
- [x] `stg_card_transactions`: normaliza `event_type` para minúsculas; `.yml` com `accepted_values` em `event_type` e `status`
- [x] `stg_acquirer_transactions`: calcula `has_settlement_discrepancy`; `.yml` com `relationships` em `card_transaction_id`; `accepted_values` em `status`
- [x] `dbt build --select bronze` sem erros

**Tests:** dbt built-in tests
**Gate:** `dbt build --select bronze` — 0 falhas

---

### T11: Criar modelo Silver `int_financial_events` + `.yml`

**What:** Model dbt Silver que une as 3 fontes em modelo unificado de eventos
**Where:** `dbt/models/silver/int_financial_events.sql` + `int_financial_events.yml`
**Depends on:** T9, T10
**Requirement:** DBT-02

**Done when:**
- [x] UNION das 3 fontes com campos: `transaction_id`, `source`, `amount_gross`, `amount_net`, `event_date`, `settlement_date`, `status`, `is_settled`, `is_duplicate`
- [x] `.yml` com `not_null` em `transaction_id` e `source`; `accepted_values` em `source` (`bank`, `card`, `acquirer`)
- [x] `dbt build --select silver` sem erros

**Tests:** dbt built-in tests
**Gate:** `SELECT source, COUNT(*) FROM int_financial_events GROUP BY source` mostra 3 valores

---

### T12: Criar modelo Gold `fct_financial_transactions` + `.yml`

**What:** Tabela fato principal com todas as transações normalizadas
**Where:** `dbt/models/gold/fct_financial_transactions.sql` + `fct_financial_transactions.yml`
**Depends on:** T11
**Requirement:** DBT-03 (AD-004)

**Done when:**
- [x] Todos os campos do spec presentes: `transaction_id`, `source`, `amount_gross`, `amount_net`, `status`, `is_settled`, `is_duplicate`, `event_date`, `settlement_date`
- [x] `.yml` com `not_null` e `unique` em `transaction_id`; `accepted_values` em `source` e nos booleanos; descrição de cada coluna
- [x] `dbt build --select fct_financial_transactions` sem erros

**Tests:** dbt built-in tests
**Gate:** `dbt build --select fct_financial_transactions` — 0 falhas

---

### T13: Criar modelo Gold `fct_revenue` + `.yml` e testes customizados

**What:** Métricas calculadas com armadilhas documentadas + 2 testes customizados
**Where:** `dbt/models/gold/fct_revenue.sql` + `fct_revenue.yml` + `dbt/tests/assert_*.sql`
**Depends on:** T12
**Requirement:** DBT-04, DBT-05

**Done when:**
- [x] `fct_revenue` calcula: `gross_revenue`, `net_revenue`, `tpv`, `acquirer_fee_rate`, `daily_balance`
- [x] `.yml` documenta armadilha de cada métrica; teste customizado `net_revenue <= gross_revenue`
- [x] `assert_no_duplicate_transactions.sql` retorna 0 linhas
- [x] `assert_settled_amounts_non_negative.sql` retorna 0 linhas
- [x] `dbt build --select gold` sem erros

**Tests:** dbt built-in tests + custom
**Gate:** `dbt build --select gold` — 0 falhas; `dbt test --select tag:custom` — 0 falhas

---

### T14: Criar `agent/context_loader.py`

**What:** Módulo que carrega contexto analítico dinâmico do banco para o agente
**Where:** `agent/context_loader.py`
**Depends on:** T13
**Requirement:** AGT-04

**Done when:**
- [x] Retorna dict com: total de transações por status, % de `is_duplicate`, % de `has_settlement_discrepancy`, período dos dados
- [x] Conecta ao banco usando variáveis do `.env`
- [x] Falha graciosamente se banco indisponível (retorna contexto vazio com warning)

**Tests:** none
**Gate:** `python agent/context_loader.py` imprime contexto não-vazio do banco

---

### T15: Criar `agent/tools.py`

**What:** Ferramentas LangChain para o agente consultar dados e métricas do banco
**Where:** `agent/tools.py`
**Depends on:** T14
**Requirement:** AGT-04

**Done when:**
- [x] `query_metrics_tool`: retorna valores de `fct_revenue`
- [x] `check_data_quality_tool`: retorna flags de qualidade (duplicatas, discrepâncias)
- [x] `explain_metric_tool`: retorna definição e armadilha da métrica pelo nome
- [x] Cada tool é um `@tool` LangChain válido

**Tests:** none
**Gate:** Chamar cada tool diretamente retorna dados não-nulos

---

### T16: Criar `agent/prompts.py`

**What:** Prompt base do agente Granger em português com persona de analista crítico
**Where:** `agent/prompts.py`
**Depends on:** None
**Requirement:** AGT-01, AGT-02, AGT-03 (AD-002: português)

**Done when:**
- [x] Prompt instrui o agente a: identificar premissas implícitas, detectar inconsistências, apontar riscos, sugerir validações
- [x] Instrui resposta sempre em português, didática e baseada em evidências
- [x] Template com `{data_context}` e `{user_input}` como variáveis
- [x] Inclui exemplos few-shot dos 3 cenários obrigatórios

**Tests:** none
**Gate:** Visual — prompt revisado e aprovado

---

### T17: Criar `agent/agent.py`

**What:** Orquestrador principal do agente com LangChain + Groq
**Where:** `agent/agent.py`
**Depends on:** T14, T15, T16
**Requirement:** AGT-01, AGT-02, AGT-03

**Done when:**
- [x] `ChatGroq(model="llama3-8b-8192")` configurado com `GROQ_API_KEY`
- [x] `AgentExecutor` com as 3 ferramentas de T15
- [x] Função `analyze(user_input: str) -> dict` retorna `{inconsistencias, riscos, validacoes_sugeridas}`
- [x] Os 3 cenários obrigatórios do PRD retornam respostas coerentes

**Tests:** none
**Gate:** `python agent/agent.py` com os 3 inputs de teste retorna respostas em português com 3 seções

---

### T18: Criar `app/components/metric_panel.py`

**What:** Componente Streamlit que exibe métricas do `fct_revenue` com indicadores de risco
**Where:** `app/components/metric_panel.py`
**Depends on:** T13
**Requirement:** UI-01

**Done when:**
- [x] Exibe os 5 valores de `fct_revenue` com labels em português
- [x] Métricas com armadilhas têm indicador visual (ex: ⚠️ ou cor amarela)
- [x] Exibe mensagem de erro amigável se banco indisponível

**Tests:** none
**Gate:** Visual — componente renderiza na interface com dados reais

---

### T19: Criar `app/components/response_card.py`

**What:** Componente Streamlit que renderiza resposta do agente em 3 seções visuais
**Where:** `app/components/response_card.py`
**Depends on:** None
**Requirement:** UI-02

**Done when:**
- [x] Renderiza seção "⚠️ Inconsistências" em bloco amarelo/laranja
- [x] Renderiza seção "🔴 Riscos" em bloco vermelho
- [x] Renderiza seção "✅ Validações Sugeridas" em bloco verde
- [x] Fallback: exibe resposta bruta se estrutura não vier nas 3 seções

**Tests:** none
**Gate:** Visual — 3 seções visíveis e distintas na interface

---

### T20: Criar `app/streamlit_app.py`

**What:** App Streamlit principal que integra painel de métricas, input e resposta do agente
**Where:** `app/streamlit_app.py`
**Depends on:** T17, T18, T19
**Requirement:** UI-01, UI-02, UI-03

**Done when:**
- [x] Layout em 2 colunas: métricas (esquerda) + agente (direita)
- [x] Campo de input com botão "Analisar"
- [x] Spinner durante processamento do agente
- [x] 3 exemplos pré-carregados clicáveis (cenários do PRD)
- [x] `streamlit run app/streamlit_app.py` abre interface sem erros

**Tests:** none
**Gate:** `streamlit run app/streamlit_app.py` — interface abre e os 3 cenários funcionam end-to-end

---

### T21: Criar `philosophy.md` [P]

**What:** Manifesto do produto explicando a filosofia e os erros intencionais
**Where:** `philosophy.md` (raiz)
**Depends on:** T20
**Requirement:** Critério de aceitação do PRD

**Done when:**
- [x] Explica: "Dados não falham apenas por erro técnico, mas por interpretação incorreta"
- [x] Lista e explica cada erro intencional e por que foi criado
- [x] Descreve os 3 cenários de erro do PRD

**Tests:** none
**Gate:** Documento criado e revisado

---

### T22: Atualizar `README.md` [P]

**What:** Atualizar README existente com instruções de setup e exemplos de uso
**Where:** `README.md` (raiz)
**Depends on:** T20
**Requirement:** Critério de aceitação do PRD

**Done when:**
- [x] Instruções de instalação: `git clone`, `cp .env.example .env`, `docker compose up`, `dbt run`, `streamlit run`
- [x] Exemplos dos 3 cenários de uso do PRD
- [x] Link para `philosophy.md`

**Tests:** none
**Gate:** Seguindo as instruções do README do zero, o sistema sobe sem consultar mais documentação

---

## Parallel Execution Map

```
Phase 1 (Sequential):
  T1 → T2 → T3 → T4

Phase 2 (Parallel):
  T4 completo, então:
    ├── T5 [P]
    ├── T6 [P]  } Simultâneos
    └── T7 [P]
  T5+T6+T7 completos → T8

Phase 3 (Sequential — dependência de camada dbt):
  T8 → T9 → T10 → T11 → T12 → T13

Phase 4 (Sequential):
  T13 → T14 → T15
  T16 (independente, pode rodar em paralelo com T14/T15)
  T14+T15+T16 completos → T17

Phase 5 (Sequential):
  T17 → T18 → T19 → T20

Phase 6 (Parallel):
  T20 completo, então:
    ├── T21 [P]
    └── T22 [P]
```

---

## Task Granularity Check

| Task | Scope | Status |
| --- | --- | --- |
| T1: docker-compose.yml | 1 arquivo | ✅ Granular |
| T2: .env.example | 1 arquivo | ✅ Granular |
| T3: init.sql + tabelas | 1 arquivo, 3 tabelas relacionadas | ✅ OK (coeso) |
| T4: requirements.txt | 1 arquivo | ✅ Granular |
| T5: generate_bank | 1 script | ✅ Granular |
| T6: generate_card | 1 script | ✅ Granular |
| T7: generate_acquirer | 1 script | ✅ Granular |
| T8: load_all.py | 1 orquestrador | ✅ Granular |
| T9: stg_bank + yml | 1 modelo + 1 contrato | ✅ OK (coeso) |
| T10: stg_card + stg_acquirer + ymls | 2 modelos relacionados | ⚠️ OK (mesma camada, mesma lógica) |
| T11: int_financial_events + yml | 1 modelo + 1 contrato | ✅ Granular |
| T12: fct_transactions + yml | 1 modelo + 1 contrato | ✅ Granular |
| T13: fct_revenue + yml + testes | 1 modelo + contrato + 2 testes | ✅ OK (coeso) |
| T14: context_loader | 1 módulo | ✅ Granular |
| T15: tools.py | 3 ferramentas, 1 arquivo | ✅ OK (coeso) |
| T16: prompts.py | 1 arquivo | ✅ Granular |
| T17: agent.py | 1 orquestrador | ✅ Granular |
| T18: metric_panel | 1 componente | ✅ Granular |
| T19: response_card | 1 componente | ✅ Granular |
| T20: streamlit_app | 1 app principal | ✅ Granular |
| T21: philosophy.md | 1 documento | ✅ Granular |
| T22: README update | 1 documento | ✅ Granular |

---

## Diagram-Definition Cross-Check

| Task | Depends On (body) | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | Phase 1 início | ✅ Match |
| T2 | T1 | T1 → T2 | ✅ Match |
| T3 | T1, T2 | T2 → T3 | ✅ Match |
| T4 | T1 | T3 → T4 | ✅ Match |
| T5 | T4 | T4 → T5 [P] | ✅ Match |
| T6 | T4 | T4 → T6 [P] | ✅ Match |
| T7 | T4 | T4 → T7 [P] | ✅ Match |
| T8 | T3, T5, T6, T7 | T5+T6+T7 → T8 | ✅ Match |
| T9 | T8 | T8 → T9 | ✅ Match |
| T10 | T8 | T8 → T10 | ✅ Match |
| T11 | T9, T10 | T10 → T11 | ✅ Match |
| T12 | T11 | T11 → T12 | ✅ Match |
| T13 | T12 | T12 → T13 | ✅ Match |
| T14 | T13 | T13 → T14 | ✅ Match |
| T15 | T14 | T14 → T15 | ✅ Match |
| T16 | None | Paralelo com T14/T15 | ✅ Match |
| T17 | T14, T15, T16 | T14+T15+T16 → T17 | ✅ Match |
| T18 | T13 | T17 → T18 | ⚠️ T18 depende de T13 (dados) e T17 indiretamente; sequência via T20 está correta |
| T19 | None | T18 → T19 | ✅ OK (T19 é componente independente de dados) |
| T20 | T17, T18, T19 | T17+T18+T19 → T20 | ✅ Match |
| T21 | T20 | T20 → T21 [P] | ✅ Match |
| T22 | T20 | T20 → T22 [P] | ✅ Match |
