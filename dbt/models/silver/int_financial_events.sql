{{ config(materialized='view') }}

WITH bank AS (
    SELECT 
        transaction_id,
        'bank' as source,
        amount as amount_gross,
        amount as amount_net,
        event_date,
        processing_date as settlement_date,
        status,
        CASE WHEN status = 'processed' THEN TRUE ELSE FALSE END as is_settled,
        FALSE as is_duplicate
    FROM {{ ref('stg_bank_transactions') }}
),

card AS (
    SELECT 
        transaction_id,
        'card' as source,
        amount as amount_gross,
        captured_amount as amount_net,
        event_date,
        NULL::timestamp as settlement_date,
        status,
        FALSE as is_settled,
        FALSE as is_duplicate
    FROM {{ ref('stg_card_transactions') }}
),

acquirer AS (
    SELECT 
        transaction_id,
        'acquirer' as source,
        amount_gross,
        amount_net,
        NULL::timestamp as event_date,
        settlement_date::timestamp as settlement_date,
        status,
        CASE WHEN status = 'settled' THEN TRUE ELSE FALSE END as is_settled,
        FALSE as is_duplicate
    FROM {{ ref('stg_acquirer_transactions') }}
)

SELECT * FROM bank
UNION ALL
SELECT * FROM card
UNION ALL
SELECT * FROM acquirer
