-- Teste para garantir que duplicatas intencionais são rastreáveis via flag, 
-- mas não devem existir sem estarem marcadas.
SELECT
    transaction_id,
    count(*)
FROM {{ ref('fct_financial_transactions') }}
WHERE NOT is_duplicate
GROUP BY 1
HAVING count(*) > 1
