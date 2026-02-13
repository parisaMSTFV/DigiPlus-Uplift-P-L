-- Template SQL: build daily customer activity table for uplift calculation
-- Replace placeholders with your warehouse tables and filters.

WITH base AS (
  SELECT
    customer_id,
    order_date::date AS day,
    rfm_segment,
    -- plus_flag: 1 if customer is Plus-active on that day
    plus_flag,
    orders,
    items,
    nmv,
    pc1_profit,
    shipping_profit
  FROM {{activity_table}}
  WHERE order_date >= {{start_date}} AND order_date < {{end_date}}
)
SELECT * FROM base;
