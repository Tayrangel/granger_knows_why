# Agente Crítico (LangChain + Groq) — Specification

## Problem Statement

O coração do produto é um agente que não responde perguntas — ele questiona respostas. Analistas submetem queries SQL, nomes de métricas ou conclusões textuais e recebem de volta inconsistências, riscos e sugestões de validação. Sem o agente, o sistema é apenas um pipeline de dados convencional.

## Goals

- [ ] Agente identifica inconsistências em pelo menos 3 cenários simulados obrigatórios do PRD
- [ ] Respostas são coerentes com o contexto dos dados e citam fontes analíticas quando possível

## Out of Scope

| Feature | Reason |
| --- | --- |
| Execução de SQL pelo agente | LLM interpreta, não executa |
| Memória persistente de conversas | MVP sem histórico por sessão |
| Suporte a múltiplos LLMs | Apenas Groq + LLaMA 3 no MVP |

---

## User Stories

### P1: Agente responde a conclusão textual ⭐ MVP

**User Story:** Como analytics engineer, quero submeter uma conclusão analítica em português (ex: "Receita bruta aumentou 20% no mês") e receber do agente uma análise crítica estruturada com inconsistências, riscos e validações sugeridas.

**Why P1:** É o cenário de uso mais simples e demonstra o valor principal do produto.

**Acceptance Criteria:**

1. WHEN o usuário submete texto analítico THEN system SHALL o agente retornar resposta em português com 3 seções: `inconsistências`, `riscos`, `validações sugeridas`
2. WHEN o input é "Receita bruta aumentou 20%" THEN system SHALL o agente questionar se transações não liquidadas foram incluídas no cálculo
3. WHEN o agente responde THEN system SHALL a resposta ser baseada no contexto dos dados reais do banco (via `context_loader`)

**Independent Test:** Submeter "Receita bruta aumentou 20% no mês" e verificar que a resposta menciona transações não liquidadas ou `status = 'pending'`.

---

### P1: Agente analisa query SQL ⭐ MVP

**User Story:** Como analytics engineer, quero submeter uma query SQL e receber do agente a identificação de problemas lógicos, duplicidades ou ausência de filtros importantes.

**Why P1:** Cenário #2 obrigatório do PRD: SQL com `SELECT SUM(amount) FROM card_transactions` sem filtro de `event_type`.

**Acceptance Criteria:**

1. WHEN o usuário submete SQL THEN system SHALL o agente identificar ausência de filtros críticos (ex: `event_type`, `status`)
2. WHEN SQL sem filtro de `event_type` em `card_transactions` é submetido THEN system SHALL o agente apontar risco de dupla contagem entre autorização e captura
3. WHEN o agente responde sobre SQL THEN system SHALL sugerir a query corrigida ou o filtro ausente

**Independent Test:** Submeter `SELECT SUM(amount) FROM card_transactions` e verificar que a resposta menciona duplicidade entre `authorization` e `capture`.

---

### P1: Agente responde a nome de métrica ⭐ MVP

**User Story:** Como analytics engineer, quero submeter apenas o nome de uma métrica (ex: "TPV") e receber do agente explicação das armadilhas associadas e como evitá-las.

**Why P1:** Cenário #3 obrigatório do PRD: "TPV do mês foi R$ 500k" pode ter dupla contagem.

**Acceptance Criteria:**

1. WHEN o usuário submete "TPV" THEN system SHALL o agente retornar definição da métrica e suas armadilhas documentadas
2. WHEN "TPV" é submetido THEN system SHALL o agente mencionar risco de dupla contagem entre `card_transactions` e `acquirer_transactions`
3. WHEN a métrica é reconhecida THEN system SHALL o agente fornecer o valor atual do banco como contexto

**Independent Test:** Submeter "TPV" e verificar que a resposta menciona dupla contagem.

---

### P2: Ferramentas do agente com contexto do banco

**User Story:** Como desenvolvedor, quero que o agente use ferramentas LangChain para consultar dados reais do banco como contexto, tornando as respostas baseadas em evidências.

**Why P2:** Sem contexto real, o agente é genérico. Com contexto, as respostas são específicas e confiáveis.

**Acceptance Criteria:**

1. WHEN o agente é invocado THEN system SHALL carregar automaticamente: total de transações por status, % de registros com flags de qualidade, período dos dados
2. WHEN `query_metrics_tool` é chamada THEN system SHALL retornar valores atuais de `fct_revenue`
3. WHEN `check_data_quality_tool` é chamada THEN system SHALL retornar contagem de `is_duplicate` e `has_settlement_discrepancy`

**Independent Test:** Chamar cada tool diretamente e verificar que retornam dados não-nulos do banco.

---

## Edge Cases

- WHEN a `GROQ_API_KEY` é inválida ou ausente THEN system SHALL falhar com mensagem de erro clara
- WHEN o banco está indisponível THEN system SHALL retornar resposta genérica sem context loader (degradação graciosa)
- WHEN o input é vazio THEN system SHALL solicitar que o usuário forneça uma query, métrica ou conclusão

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| AGT-01 | P1: Resposta a texto analítico | Tasks | Pending |
| AGT-02 | P1: Análise de SQL | Tasks | Pending |
| AGT-03 | P1: Resposta a nome de métrica | Tasks | Pending |
| AGT-04 | P2: Ferramentas com contexto do banco | Tasks | Pending |

---

## Success Criteria

- [ ] Os 3 cenários obrigatórios do PRD produzem respostas corretas e coerentes
- [ ] Respostas sempre em português, com as 3 seções estruturadas
- [ ] Ferramentas retornam dados reais do banco como contexto
