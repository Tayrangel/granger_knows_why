# Filosofia do Granger Knows Why

O Granger não é apenas um chatbot financeiro. Ele é uma camada de **pensamento crítico** sobre os dados.

## Por que "Granger"?
O nome é inspirado na necessidade de um rigor acadêmico e crítico. Granger não aceita respostas fáceis. Se o dado diz que a receita subiu, Granger pergunta: "Mas de que tipo de receita estamos falando? Ela já caiu no caixa?"

## Armadilhas Analíticas Intencionais
Para demonstrar o valor do agente, os dados simulados neste projeto contêm erros clássicos de análise:

1. **Inflação de Receita (Pending Transactions)**:
   - A métrica de "Receita Bruta" inclui transações com status `pending`. 
   - Analistas juniores podem reportar esse valor como receita real, mas ela pode nunca ser liquidada.

2. **TPV Duplicado (Auth vs Capture)**:
   - Queries simples em `card_transactions` somam autorizações e capturas.
   - Isso triplica o volume transacional real se não houver filtro por `event_type`.

3. **Discrepância de Liquidação (Settlement Gap)**:
   - Algumas transações no adquirente têm `amount_net` calculado incorretamente, ignorando a taxa (`fee`).
   - Isso distorce a margem real e a reconciliação com o banco.

## O Papel do Agente
O agente utiliza o contexto do banco de dados (via `context_loader`) e ferramentas específicas (via `tools`) para confrontar o que o usuário diz com a realidade técnica dos dados. 

**O objetivo final não é dar a resposta certa, mas evitar a resposta errada.**
