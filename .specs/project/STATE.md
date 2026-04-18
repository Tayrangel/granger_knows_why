# State

**Last Updated:** 2026-04-18T14:51:00-03:00
**Current Work:** Planejamento MVP — criação de documentos tlc-spec-driven

---

## Recent Decisions (Last 60 days)

### AD-001: LLM escolhido — Groq + LLaMA 3 (2026-04-18)

**Decision:** Usar Groq + LLaMA 3 (`langchain-groq`, modelo `llama3-8b-8192`) como LLM do agente
**Reason:** Gratuito, rápido, sem necessidade de API key paga; suficiente para o escopo do MVP
**Trade-off:** Pode ter raciocínio menos profundo que GPT-4o em edge cases; sem fallback automático
**Impact:** Requer `GROQ_API_KEY` no `.env`; usar `llama3-70b-8192` se qualidade for insuficiente

### AD-002: Idioma da interface e do agente — Português (2026-04-18)

**Decision:** Interface Streamlit e todas as respostas do agente em português
**Reason:** Alinhado com o público-alvo e com o PRD (redigido em português)
**Trade-off:** README existente está em inglês; será mantido em inglês para audiência global
**Impact:** Prompt do agente deve instrur respostas em português; labels da UI em português

### AD-003: Volume de dados simulados fixado (2026-04-18)

**Decision:** ~3.700 registros (bank: 1.000 | card: 1.500 | acquirer: 1.200)
**Reason:** Suficiente para demonstrar os 3 cenários de erro obrigatórios do PRD
**Trade-off:** Não simula ambiente enterprise realista
**Impact:** Scripts de seed devem atingir exatamente esses volumes

### AD-004: Contrato de dados obrigatório por modelo dbt (2026-04-18)

**Decision:** Cada arquivo `.sql` em Bronze, Silver e Gold deve ter um `.yml` correspondente com `data_tests`
**Reason:** Garante rastreabilidade e qualidade dos dados em todas as camadas
**Trade-off:** Adiciona tempo de criação; necessário para critérios de aceitação do PRD
**Impact:** `not_null`, `unique`, `accepted_values`, `relationships` por camada

### AD-005: Campo `direction` renomeado para `payment_method` em bank_transactions (2026-04-18)

**Decision:** O campo que indica crédito/débito na tabela `bank_transactions` se chama `payment_method`
**Reason:** Melhor semântica de domínio financeiro
**Trade-off:** Nenhum (greenfield)
**Impact:** Scripts de seed, modelos dbt e contratos `.yml` devem usar `payment_method`

---

## Active Blockers

_Nenhum no momento._

---

## Lessons Learned

_Nenhum ainda — projeto em fase de planejamento._

---

## Quick Tasks Completed

| #   | Description | Date | Commit | Status |
| --- | --- | --- | --- | --- |
| — | — | — | — | — |

---

## Deferred Ideas

- [ ] Integração com linhagem do dbt (dbt docs) — Capturado durante: planejamento MVP
- [ ] Observabilidade de pipeline em tempo real — Capturado durante: planejamento MVP
- [ ] Suporte a múltiplos LLMs com fallback automático — Capturado durante: AD-001

---

## Todos

- [ ] Confirmar estrutura de diretórios do projeto com o usuário antes de iniciar Fase 1
- [ ] Obter `GROQ_API_KEY` antes de iniciar Fase 4 (agente)

---

## Preferences

**Model Guidance Shown:** 2026-04-18
