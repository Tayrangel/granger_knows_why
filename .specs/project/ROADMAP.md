# Roadmap

**Current Milestone:** M1 — MVP Completo
**Status:** Planning

---

## M1 — MVP Completo

**Goal:** Sistema funcionando de ponta a ponta: dados simulados → dbt → agente crítico → interface Streamlit
**Target:** Pronto para demonstração dos 3 cenários de erro obrigatórios do PRD

---

### Features

**Setup de Ambiente** — PLANNED

- Docker Compose com PostgreSQL (`granger_db`) e Streamlit
- Variáveis de ambiente via `.env`
- Banco de dados inicializado e acessível

**Geração e Ingestão de Dados Simulados** — PLANNED

- Script Python + Faker gerando `bank_transactions` (~1.000 linhas)
- Script Python + Faker gerando `card_transactions` (~1.500 linhas)
- Script Python + Faker gerando `acquirer_transactions` (~1.200 linhas)
- Erros intencionais controlados: status inconsistentes, duplicidades, cancelamentos parciais
- Dados carregados no PostgreSQL via script `load_all.py`

**Modelagem dbt — Bronze/Silver/Gold** — PLANNED

- Bronze: `stg_bank_transactions`, `stg_card_transactions`, `stg_acquirer_transactions` (+ `.yml` com `data_tests`)
- Silver: `int_financial_events` (+ `.yml`)
- Gold: `fct_financial_transactions`, `fct_revenue` (+ `.yml` com armadilhas documentadas)
- Testes dbt customizados: `assert_no_duplicate_transactions`, `assert_settled_amounts_non_negative`

**Agente Inteligente (LangChain + Groq)** — PLANNED

- Prompt base em português com persona de analista crítico
- Ferramentas: `query_metrics_tool`, `check_data_quality_tool`, `explain_metric_tool`
- Suporte a 3 tipos de input: SQL livre, nome de métrica, conclusão textual
- Output estruturado: inconsistências, riscos, validações sugeridas

**Interface Streamlit** — PLANNED

- Painel de métricas em tempo real (consumindo `fct_revenue`)
- Input livre (SQL / texto / nome de métrica)
- Resposta estruturada do agente com seções visuais
- Indicadores de risco nas métricas

**Documentação e Narrativa** — PLANNED

- `philosophy.md` — manifesto do produto
- `README.md` atualizado com instruções de setup e cenários de uso
- 3 cenários de erro documentados e demonstráveis

---

## M2 — Qualidade e Observabilidade (Futuro)

**Goal:** Tornar o sistema mais robusto e observável

### Features

**Linhagem dbt** — PLANNED
**Observabilidade de pipeline** — PLANNED
**Suporte a múltiplos LLMs com fallback** — PLANNED

---

## Future Considerations

- Integração com sistemas de dados reais (com autenticação)
- Deploy em cloud (Streamlit Cloud, Railway, Render)
- Suporte a múltiplos idiomas
- Dashboard de qualidade de dados em tempo real
