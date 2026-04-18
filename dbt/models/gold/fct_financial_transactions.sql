{{ config(materialized='table') }}

SELECT
    transaction_id,
    source,
    amount_gross,
    amount_net,
    status,
    is_settled,
    is_duplicate,
    event_date,
    settlement_date
FROM {{ ref('int_financial_events') }}
