from __future__ import annotations

import pandas as pd

from rfm.policy import build_segment_action_plan


def test_build_segment_action_plan_outputs_decision_columns() -> None:
    summary = pd.DataFrame(
        {
            "rule_label": ["High Value", "Loyal", "Regular", "Hibernating"],
            "customer_count": [40, 30, 20, 10],
            "estimated_ltv_total": [10000.0, 6000.0, 1500.0, 300.0],
            "estimated_ltv_share": [0.56, 0.34, 0.08, 0.02],
        }
    )
    out = build_segment_action_plan(summary, segment_col="rule_label")

    required = {"priority_tier", "objective", "recommended_action", "channel", "spend_guidance"}
    assert required.issubset(out.columns)
    assert out["priority_tier"].notna().all()
    assert out["recommended_action"].str.len().gt(0).all()
