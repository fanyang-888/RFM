from __future__ import annotations

import numpy as np
import pandas as pd


def _safe_qcut(values: pd.Series, q: int, labels: list[str]) -> pd.Series:
    """Return quantile bins and handle low-cardinality edge cases."""
    try:
        return pd.qcut(values, q=q, labels=labels, duplicates="drop")
    except ValueError:
        ranked = values.rank(method="first")
        return pd.qcut(ranked, q=q, labels=labels, duplicates="drop")


def estimate_customer_ltv(
    rfm: pd.DataFrame,
    recency_half_life_days: float = 180.0,
    margin_rate: float = 1.0,
) -> pd.DataFrame:
    """
    Estimate customer-level expected value with an interpretable heuristic.

    Assumptions:
    - More recent buyers have higher near-term repeat probability.
    - Higher purchase frequency implies stronger future value potential.
    - Monetary value from observed history is the value baseline.
    """
    required_cols = {"Recency", "Frequency", "Monetary"}
    missing_cols = required_cols.difference(rfm.columns)
    if missing_cols:
        missing = ", ".join(sorted(missing_cols))
        raise ValueError(f"Missing required columns for LTV estimation: {missing}")

    out = rfm.copy()

    recency_weight = np.exp(-np.log(2.0) * out["Recency"] / recency_half_life_days)
    frequency_multiplier = 1.0 + np.log1p(out["Frequency"].clip(lower=0.0))

    out["recency_weight"] = recency_weight
    out["frequency_multiplier"] = frequency_multiplier
    out["estimated_ltv"] = out["Monetary"] * recency_weight * frequency_multiplier * margin_rate

    out["estimated_ltv_rank_pct"] = out["estimated_ltv"].rank(pct=True, ascending=True)
    out["value_tier"] = _safe_qcut(
        out["estimated_ltv_rank_pct"],
        q=3,
        labels=["Low Value", "Mid Value", "High Value"],
    ).astype(str)
    return out


def summarize_ltv_by_segment(
    ltv_table: pd.DataFrame,
    segment_col: str = "rule_label",
) -> pd.DataFrame:
    """Aggregate value metrics to segment-level decision view."""
    if segment_col not in ltv_table.columns:
        raise ValueError(f"Column '{segment_col}' is required for segment summary.")

    summary = (
        ltv_table.groupby(segment_col, dropna=False)
        .agg(
            customer_count=("estimated_ltv", "size"),
            monetary_observed=("Monetary", "sum"),
            avg_monetary=("Monetary", "mean"),
            estimated_ltv_total=("estimated_ltv", "sum"),
            estimated_ltv_avg=("estimated_ltv", "mean"),
            recency_avg=("Recency", "mean"),
            frequency_avg=("Frequency", "mean"),
        )
        .reset_index()
    )

    total_ltv = summary["estimated_ltv_total"].sum()
    if total_ltv > 0:
        summary["estimated_ltv_share"] = summary["estimated_ltv_total"] / total_ltv
    else:
        summary["estimated_ltv_share"] = 0.0

    summary = summary.sort_values("estimated_ltv_total", ascending=False).reset_index(drop=True)
    return summary
