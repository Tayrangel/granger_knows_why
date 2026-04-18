{{ config(materialized='view') }}

WITH raw_data AS (
    SELECT * FROM {{ source('raw', 'card_transactions') }}
)

SELECT
    transaction_id,
    authorization_id,
    amount,
    captured_amount,
    LOWER(event_type) as event_type,
    status,
    event_date
FROM raw_data
