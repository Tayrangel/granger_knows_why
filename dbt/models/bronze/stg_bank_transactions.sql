{{ config(materialized='view') }}

WITH raw_data AS (
    SELECT * FROM {{ source('raw', 'bank_transactions') }}
)

SELECT
    transaction_id,
    amount,
    payment_method,
    balance_after,
    event_date,
    processing_date,
    status
FROM raw_data
