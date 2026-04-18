# Tasks Plan

## Bloco 1 — Setup do ambiente
- Criar repositório GitHub
- Configurar Docker
- Subir PostgreSQL via container
- Criar banco `granger_db`

## Bloco 2 — Geração de dados
- Criar script Python com Faker
- Gerar:
bank_transactions;
card_transactions;
acquirer_transactions.
- Inserir no PostgreSQL

👉 Aqui você controla os erros intencionais

## Bloco 3 — dbt
- Inicializar projeto dbt
- Criar models:
Bronze
stg_bank_transactions
stg_card_transactions
stg_acquirer_transactions

Silver
int_financial_events

Gold
fct_financial_transactions
fct_revenue

## Bloco 4 — Métricas
- Criar métricas com problemas:
receita inflada;
TPV duplicado.

- Criar testes dbt básicos

## Bloco 5 — Agente
- Setup LangChain
- Criar prompt base (personalidade Hermione)
- Conectar com:
métricas;
SQL.

- Criar função de análise

## Bloco 6 — Interface
- Criar app com Streamlit
- Input de pergunta
- Exibir resposta do agente

## Bloco 7 — Narrativa
- Criar `philosophy.md`
- Criar cenários de erro
- Refinar README