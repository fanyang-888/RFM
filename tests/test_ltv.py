from __future__ import annotations

import pandas as pd

from rfm.ltv import estimate_customer_ltv, summarize_ltv_by_segment


def _sample_rfm() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Recency": [10.0, 20.0, 120.0, 200.0],
            "Frequency": [12.0, 6.0, 3.0, 1.0],
            "Monetary": [800.0, 320.0, 150.0, 40.0],
            "rule_label": ["High Value", "Loyal", "Regular", "Hibernating"],
        },
        index=[1001, 1002, 1003, 1004],
    )


def test_estimate_customer_ltv_adds_expected_columns() -> None:
    out = estimate_customer_ltv(_sample_rfm())
    expected_cols = {
        "recency_weight",
        "frequency_multiplier",
        "estimated_ltv",
        "estimated_ltv_rank_pct",
        "value_tier",
    }
    assert expected_cols.issubset(out.columns)
    assert out["estimated_ltv"].gt(0).all()


def test_estimated_ltv_monotonicity_sanity() -> None:
    out = estimate_customer_ltv(_sample_rfm())
    ordered = out.sort_values("Monetary", ascending=False)
    assert ordered.iloc[0]["estimated_ltv"] >= ordered.iloc[-1]["estimated_ltv"]


def test_segment_summary_integrity() -> None:
    ltv = estimate_customer_ltv(_sample_rfm())
    summary = summarize_ltv_by_segment(ltv, segment_col="rule_label")
    assert {"customer_count", "estimated_ltv_total", "estimated_ltv_share"}.issubset(
        summary.columns
    )
    assert int(summary["customer_count"].sum()) == len(ltv)
    assert abs(float(summary["estimated_ltv_share"].sum()) - 1.0) < 1e-6
