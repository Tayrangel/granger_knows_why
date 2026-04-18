# Interface Streamlit — Specification

## Problem Statement

O agente precisa de uma interface onde o usuário possa submeter inputs (SQL, texto, nome de métrica) e visualizar tanto as métricas do banco quanto a análise crítica do agente. Sem interface, o produto não é demonstrável para analistas e engenheiros de dados.

## Goals

- [ ] Interface funcional e intuitiva onde o usuário interage com o agente em português
- [ ] Painel de métricas em tempo real refletindo `fct_revenue`

## Out of Scope

| Feature | Reason |
| --- | --- |
| Autenticação de usuários | Desnecessário no MVP local |
| Histórico de conversas persistido | Sem banco de sessão no MVP |
| Deploy em produção | Roda apenas localmente |

---

## User Stories

### P1: Painel de métricas ⭐ MVP

**User Story:** Como analytics engineer, quero ver as métricas principais do `fct_revenue` na interface para ter contexto antes de formular perguntas ao agente.

**Why P1:** O usuário precisa ver os números para saber o que questionar.

**Acceptance Criteria:**

1. WHEN a interface carrega THEN system SHALL exibir: Receita Bruta, Receita Líquida, TPV, Taxa de Adquirência e Saldo Diário
2. WHEN uma métrica tem risco associado (ex: inclui não liquidadas) THEN system SHALL exibir indicador visual de risco (ícone ou cor)
3. WHEN o banco está indisponível THEN system SHALL exibir mensagem de erro amigável

**Independent Test:** Abrir a interface e verificar que os 5 valores de `fct_revenue` aparecem corretamente.

---

### P1: Input do agente e resposta estruturada ⭐ MVP

**User Story:** Como analytics engineer, quero um campo de input onde posso digitar SQL, nome de métrica ou conclusão textual, e receber a análise do agente em seções visuais bem definidas.

**Why P1:** É a funcionalidade central do produto — sem ela não há demonstração possível.

**Acceptance Criteria:**

1. WHEN o usuário digita no campo de input e clica em "Analisar" THEN system SHALL chamar o agente e exibir a resposta
2. WHEN o agente responde THEN system SHALL exibir a resposta em 3 seções visuais distintas: "⚠️ Inconsistências", "🔴 Riscos", "✅ Validações Sugeridas"
3. WHEN o agente está processando THEN system SHALL exibir indicador de loading (spinner)
4. WHEN o input está vazio THEN system SHALL exibir mensagem pedindo ao usuário para fornecer um input

**Independent Test:** Submeter "Receita bruta aumentou 20%" e verificar que as 3 seções aparecem na resposta.

---

### P2: Exemplos pré-carregados

**User Story:** Como usuário, quero clicar em exemplos de cenários para carregar automaticamente o input e ver o agente em ação sem precisar digitar.

**Why P2:** Facilita demonstração do produto e reduz fricção de onboarding.

**Acceptance Criteria:**

1. WHEN o usuário clica em um exemplo THEN system SHALL preencher o campo de input com o texto do exemplo
2. WHEN os exemplos são exibidos THEN system SHALL mostrar os 3 cenários obrigatórios do PRD

**Independent Test:** Clicar nos 3 exemplos e verificar que o campo é preenchido corretamente.

---

## Edge Cases

- WHEN a resposta do agente demorar mais de 30s THEN system SHALL exibir mensagem de timeout amigável
- WHEN o agente retorna resposta sem as 3 seções esperadas THEN system SHALL exibir a resposta bruta sem quebrar a UI

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| UI-01 | P1: Painel de métricas | Tasks | Pending |
| UI-02 | P1: Input e resposta estruturada | Tasks | Pending |
| UI-03 | P2: Exemplos pré-carregados | Tasks | Pending |

---

## Success Criteria

- [ ] Interface carrega sem erros após `docker compose up`
- [ ] Os 3 cenários do PRD são demonstráveis via UI em menos de 2 minutos cada
- [ ] Painel de métricas reflete dados reais do banco
