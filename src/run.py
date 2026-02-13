from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

from src.uplift.uplift_calc import compute_daily_uplift_by_rfm
from src.pnl.subscription_allocation import allocate_subscription_revenue_daily, monthly_subscription_revenue
from src.pnl.aggregate import build_profit_variants, monthly_totals

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--activity", default="data/sample/activity_daily.csv")
    parser.add_argument("--subs", default="data/sample/subscriptions.csv")
    parser.add_argument("--month_start", default="2025-04-01")
    parser.add_argument("--month_end", default="2025-05-01")
    parser.add_argument("--out_dir", default="artifacts")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    activity = pd.read_csv(args.activity)
    daily = compute_daily_uplift_by_rfm(activity, args.month_start, args.month_end, window_days=30)
    daily.to_parquet(out_dir/"daily_uplift.parquet", index=False)

    # subscription allocation
    sub_rev_month = None
    subs_path = Path(args.subs)
    if subs_path.exists():
        subs = pd.read_csv(subs_path)
        alloc = allocate_subscription_revenue_daily(subs)
        alloc.to_parquet(out_dir/"subscription_daily.parquet", index=False)
        sub_rev_month = monthly_subscription_revenue(alloc)
        sub_rev_month.to_csv(out_dir/"subscription_monthly.csv", index=False)

    enriched = build_profit_variants(daily, sub_rev_month)
    enriched.to_parquet(out_dir/"daily_uplift_enriched.parquet", index=False)

    monthly = monthly_totals(enriched)
    monthly.to_excel(out_dir/"monthly_uplift.xlsx", index=False)

    print("Done. Outputs written to:", out_dir)

if __name__ == "__main__":
    main()
