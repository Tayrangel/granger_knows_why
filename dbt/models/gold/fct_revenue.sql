{{ config(materialized='table') }}

WITH metrics AS (
    SELECT
        DATE_TRUNC('day', COALESCE(event_date, settlement_date)) as reference_date,
        -- Armadilha: gross_revenue inclui não liquidadas
        SUM(CASE WHEN source IN ('card', 'acquirer') THEN amount_gross ELSE 0 END) as gross_revenue,
        -- net_revenue: apenas o que foi liquidado ou está em processamento bancário
        SUM(CASE WHEN source = 'acquirer' AND status = 'settled' THEN amount_net ELSE 0 END) as net_revenue,
        -- TPV: soma de card e acquirer (Armadilha: pode ter duplicidade se não filtrar por source único)
        SUM(CASE WHEN source IN ('card', 'acquirer') THEN amount_gross ELSE 0 END) as tpv,
        -- Taxa de adquirência: fee / gross
        CASE 
            WHEN SUM(CASE WHEN source = 'acquirer' THEN amount_gross ELSE 0 END) > 0 
            THEN SUM(CASE WHEN source = 'acquirer' THEN (amount_gross - amount_net) ELSE 0 END) / SUM(CASE WHEN source = 'acquirer' THEN amount_gross ELSE 0 END)
            ELSE 0 
        END as acquirer_fee_rate,
        -- Saldo diário: apenas do banco
        SUM(CASE WHEN source = 'bank' THEN amount_gross ELSE 0 END) as daily_balance
    FROM {{ ref('fct_financial_transactions') }}
    GROUP BY 1
)

SELECT * FROM metrics
