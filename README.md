# Plus Uplift P&L

Daily uplift-based P&L calculation by RFM segment, aggregated to a monthly view.

## What you get
- Uplift breakdown for: orders, items, NMV
- Profit variants:
  - PC1 profit uplift
  - PC1 + shipping profit uplift
  - PC1 + shipping + allocated subscription revenue

## Run
```bash
pip install -r requirements.txt
python -m src.run --month_start 2025-04-01 --month_end 2025-05-01
```

Outputs are written to `artifacts/`.

## Data format
Use the included sample dataset in `data/sample/` to run the demo.
For your own runs, provide a CSV with these columns:
`customer_id, day, rfm_segment, plus_flag, orders, items, nmv, pc1_profit, shipping_profit`

Subscription input (optional):
`customer_id, start_date, period_in_days, payable_price`
