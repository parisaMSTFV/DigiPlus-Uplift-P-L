# Plus Uplift P&L Framework

Uplift-based P&L modeling framework to quantify the **incremental impact** of a subscription product on customer behavior.

Instead of attributing all observed subscriber activity to the subscription, this project isolates the counterfactual baseline and measures true behavioral lift at the RFM-segment level.

---

## Business Context

Classic subscription P&L overstates impact by counting total subscriber revenue and margin as subscription-driven.

However:

Observed subscriber behavior = Baseline behavior + Subscription-induced behavior

This framework estimates:

- Incremental Orders
- Incremental Items
- Incremental NMV
- Incremental Profit (multiple definitions)

The result is a defensible uplift P&L rather than a descriptive P&L.

---

## Methodology Overview

### 1. Daily Rolling Window (30 days)

For each day `d` in the target month:

- Build a rolling 30-day window `[d-29, d]`
- Segment customers by RFM
- Identify Plus-active customers on day `d`
- Identify never-Plus customers in the same RFM segment

### 2. Counterfactual Comparison

For each RFM segment `s`:

\[
uplift_m(d,s) = 
(avg_{plus,m} - avg_{nonplus,m}) \times n_{plus}
\]

Where:

- `avg_plus_m` = per-customer metric in window
- `avg_nonplus_m` = baseline per-customer metric
- `n_plus` = number of Plus-active customers in segment

Daily uplift is aggregated across segments and summed over the month.

---

## Subscription Revenue Allocation

Subscription revenue is allocated uniformly across active days.

If a customer purchases a subscription:

