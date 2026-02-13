from __future__ import annotations
import pandas as pd

def allocate_subscription_revenue_daily(subs: pd.DataFrame) -> pd.DataFrame:
    """Allocate subscription revenue uniformly over active days.

    subs columns:
      customer_id, start_date, period_in_days, payable_price
    returns daily rows: day, customer_id, daily_revenue
    """
    s = subs.copy()
    s["start_date"] = pd.to_datetime(s["start_date"])
    s["period_in_days"] = s["period_in_days"].astype(int)
    s["payable_price"] = s["payable_price"].astype(float)
    s["daily_revenue"] = s["payable_price"] / s["period_in_days"]

    rows = []
    for r in s.itertuples(index=False):
        for k in range(r.period_in_days):
            day = (r.start_date + pd.Timedelta(days=k)).date().isoformat()
            rows.append((day, int(r.customer_id), float(r.daily_revenue)))
    return pd.DataFrame(rows, columns=["day","customer_id","daily_revenue"])

def monthly_subscription_revenue(daily_alloc: pd.DataFrame) -> pd.DataFrame:
    df = daily_alloc.copy()
    df["day"] = pd.to_datetime(df["day"])
    df["month"] = df["day"].dt.to_period("M").astype(str)
    return df.groupby("month")["daily_revenue"].sum().reset_index(name="subscription_revenue")
