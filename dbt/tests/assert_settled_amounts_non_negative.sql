-- Teste para validar que valores liquidados não podem ser negativos
SELECT
    transaction_id,
    amount_net
FROM {{ ref('fct_financial_transactions') }}
WHERE is_settled
  AND amount_net < 0
