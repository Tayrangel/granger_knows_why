# Granger Knows Why

**Vision:** Um sistema de análise crítica de métricas financeiras com agente inteligente que desafia interpretações, detecta inconsistências e questiona premissas — em vez de simplesmente responder perguntas.

**For:** Analytics Engineers e Data Analysts que trabalham com métricas financeiras e precisam de uma camada crítica antes de tomar decisões baseadas em dados.

**Solves:** A má interpretação de métricas financeiras causada por diferenças entre eventos (autorização vs liquidação), inconsistências entre fontes de dados e suposições implícitas em queries SQL — levando a decisões incorretas, distorção de receita e perda de confiança nos dados.

---

## Goals

- [ ] Demonstrar valor do agente crítico em pelo menos 3 cenários simulados de erro analítico
- [ ] Produzir pipeline dbt funcional (Bronze → Silver → Gold) sem erros, com métricas e armadilhas intencionais
- [ ] Entregar interface Streamlit funcional onde o usuário pode submeter SQL, nome de métrica ou conclusão textual e receber análise crítica estruturada

---

## Tech Stack

**Core:**

- Linguagem: Python 3.11+
- Banco de dados: PostgreSQL 15 (via Docker)
- Transformação: dbt-core + dbt-postgres
- Agente: LangChain + langchain-groq
- Interface: Streamlit

**Key dependencies:**

- `faker` — geração de dados simulados
- `langchain-groq` + LLaMA 3 (llama3-8b-8192 / llama3-70b-8192)
- `psycopg2` — conexão Python → PostgreSQL
- `docker-compose` — orquestração de ambiente

---

## Scope

**v1 (MVP) inclui:**

- Geração e ingestão de dados financeiros simulados com erros intencionais controlados
- Modelagem dbt em camadas Bronze/Silver/Gold com contratos de dados (`.yml` + `data_tests`)
- Tabela fato `fct_financial_transactions` e métricas `fct_revenue` com armadilhas documentadas
- Agente LangChain (Groq + LLaMA 3) que recebe SQL, nome de métrica ou texto analítico e retorna inconsistências, riscos e sugestões de validação — em português
- Interface Streamlit com painel de métricas e resposta estruturada do agente
- Documentação: README atualizado + `philosophy.md`

**Explicitamente fora do escopo:**

- Integração com sistemas financeiros reais
- Deploy em produção / cloud
- Autenticação e segurança avançada
- Escalabilidade enterprise
- Suporte a múltiplos idiomas (somente português no MVP)

---

## Constraints

- **Técnico:** Dados são 100% simulados — sem uso de dados reais
- **LLM:** Groq + LLaMA 3 (requer `GROQ_API_KEY` gratuita em console.groq.com)
- **Volume:** ~3.700 registros simulados (bank: 1.000 | card: 1.500 | acquirer: 1.200)
- **Ambiente:** Docker obrigatório para subir PostgreSQL; Streamlit roda localmente
