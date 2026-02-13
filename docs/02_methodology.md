# Methodology (Daily Uplift by RFM)

For each day `d` in the target month and each RFM segment `s`:

1. Build a 30-day window: `[d-29, d]`
2. Compute per-customer averages for Plus customers in `s` over the window
3. Compute per-customer averages for **never-Plus** customers in `s` over the window
4. Daily uplift for metric `m`:
   `uplift_m(d,s) = (avg_plus_m(d,s) - avg_nonplus_m(d,s)) * n_plus_customers(d,s)`
5. Sum daily uplift over the month across segments.

Subscription revenue is allocated per-day:
- `daily_rev = payable_price / period_in_days`
- monthly subscription revenue is the sum of daily_rev for days that fall in the month.
