# Metric Definitions

Base activity table (per customer per day):
- `orders`: number of orders
- `items`: number of items
- `nmv`: net merchandise value proxy
- `pc1_profit`: profit proxy (PC1)
- `shipping_profit`: shipping margin proxy

Derived uplift P&L combinations in this repo:
- `uplift_orders`
- `uplift_items`
- `uplift_nmv`
- `uplift_pc1_profit`
- `uplift_pc1_plus_shipping` = pc1_profit + shipping_profit
- `uplift_total_profit` = pc1_profit + shipping_profit + subscription_revenue_allocated
