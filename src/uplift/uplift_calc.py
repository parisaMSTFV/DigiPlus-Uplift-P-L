from __future__ import annotations

import pandas as pd
from typing import Iterable, Dict, List

METRICS = ["orders", "items", "nmv", "pc1_profit", "shipping_profit"]

def compute_daily_uplift_by_rfm(
    activity: pd.DataFrame,
    month_start: str,
    month_end_exclusive: str,
    window_days: int = 30,
) -> pd.DataFrame:
    """Daily uplift by RFM segment using a rolling window.

    activity columns required:
      customer_id, day (YYYY-MM-DD), rfm_segment, plus_flag (0/1),
      orders, items, nmv, pc1_profit, shipping_profit

    non-plus group is defined as customers that never have plus_flag=1 in the full activity input.
    """
    df = activity.copy()
    df["day"] = pd.to_datetime(df["day"])
    month_start_dt = pd.to_datetime(month_start)
    month_end_dt = pd.to_datetime(month_end_exclusive)

    # determine never-plus customers
    plus_any = df.groupby("customer_id")["plus_flag"].max()
    never_plus_ids = plus_any[plus_any == 0].index
    plus_ids = plus_any[plus_any == 1].index

    # precompute for speed
    df_plus = df[df["customer_id"].isin(plus_ids)]
    df_non = df[df["customer_id"].isin(never_plus_ids)]

    days = pd.date_range(month_start_dt, month_end_dt - pd.Timedelta(days=1), freq="D")
    out_rows = []
    for d in days:
        w_start = d - pd.Timedelta(days=window_days-1)
        w_end = d

        plus_w = df_plus[(df_plus["day"] >= w_start) & (df_plus["day"] <= w_end)]
        non_w  = df_non[(df_non["day"] >= w_start) & (df_non["day"] <= w_end)]

        # plus customers considered: those active-plus on day d (plus_flag==1 on that day)
        plus_active_ids = df_plus[(df_plus["day"] == d) & (df_plus["plus_flag"] == 1)]["customer_id"].unique()
        if len(plus_active_ids) == 0:
            continue
        plus_active = plus_w[plus_w["customer_id"].isin(plus_active_ids)]

        # per-customer sums in window
        plus_cust = plus_active.groupby(["rfm_segment","customer_id"])[METRICS].sum().reset_index()
        non_cust  = non_w.groupby(["rfm_segment","customer_id"])[METRICS].sum().reset_index()

        # per-customer averages (across customers) within RFM segment
        plus_avg = plus_cust.groupby("rfm_segment")[METRICS].mean()
        non_avg  = non_cust.groupby("rfm_segment")[METRICS].mean()

        # counts of plus customers per segment
        n_plus = plus_cust.groupby("rfm_segment")["customer_id"].nunique()

        segs = sorted(set(plus_avg.index).intersection(set(non_avg.index)))
        for s in segs:
            row = {"day": d.date().isoformat(), "rfm_segment": s, "n_plus_customers": int(n_plus.get(s, 0))}
            for m in METRICS:
                uplift = (plus_avg.loc[s, m] - non_avg.loc[s, m]) * row["n_plus_customers"]
                row[f"uplift_{m}"] = float(uplift)
            out_rows.append(row)

    out = pd.DataFrame(out_rows)
    return out
