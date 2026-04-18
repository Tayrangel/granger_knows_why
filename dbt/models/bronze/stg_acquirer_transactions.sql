{{ config(materialized='view') }}

WITH raw_data AS (
    SELECT * FROM {{ source('raw', 'acquirer_transactions') }}
)

SELECT
    transaction_id,
    card_transaction_id,
    amount_gross,
    fee_amount,
    amount_net,
    settlement_date,
    status,
    -- Flag de discrepância intencional
    CASE 
        WHEN ABS(amount_gross - fee_amount - amount_net) > 0.01 THEN TRUE 
        ELSE FALSE 
    END as has_settlement_discrepancy
FROM raw_data
