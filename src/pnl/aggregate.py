from __future__ import annotations
import pandas as pd

PROFIT_VARIANTS = [
    "pc1_profit",
    "pc1_plus_shipping",
    "total_profit_with_subscription",
]

def build_profit_variants(daily_uplift: pd.DataFrame, monthly_sub_rev: pd.DataFrame | None = None) -> pd.DataFrame:
    df = daily_uplift.copy()
    df["uplift_pc1_plus_shipping"] = df["uplift_pc1_profit"] + df["uplift_shipping_profit"]

    if monthly_sub_rev is not None:
        # distribute monthly subscription revenue across segments proportionally by n_plus_customers (simple, reviewable)
        df["day"] = pd.to_datetime(df["day"])
        df["month"] = df["day"].dt.to_period("M").astype(str)
        seg_weights = df.groupby(["month","rfm_segment"])["n_plus_customers"].sum().reset_index()
        seg_total = seg_weights.groupby("month")["n_plus_customers"].sum().reset_index(name="total_plus")
        seg_weights = seg_weights.merge(seg_total, on="month", how="left")
        seg_weights["w"] = seg_weights["n_plus_customers"] / seg_weights["total_plus"].clip(lower=1)

        df = df.merge(seg_weights[["month","rfm_segment","w"]], on=["month","rfm_segment"], how="left")
        df = df.merge(monthly_sub_rev, on="month", how="left")
        df["subscription_rev_alloc"] = df["subscription_revenue"].fillna(0) * df["w"].fillna(0)
    else:
        df["subscription_rev_alloc"] = 0.0

    df["uplift_total_profit"] = df["uplift_pc1_plus_shipping"] + df["subscription_rev_alloc"]
    return df

def monthly_totals(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["day"] = pd.to_datetime(d["day"])
    d["month"] = d["day"].dt.to_period("M").astype(str)
    cols = [c for c in d.columns if c.startswith("uplift_")]
    return d.groupby("month")[cols].sum().reset_index()
