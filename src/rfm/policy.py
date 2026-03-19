from __future__ import annotations

import pandas as pd


SEGMENT_POLICY = {
    "High Value": {
        "objective": "Retain",
        "recommended_action": "VIP loyalty treatment with service guarantees",
        "channel": "Email + CRM manager outreach",
    },
    "Loyal": {
        "objective": "Retain and grow",
        "recommended_action": "Tiered loyalty rewards and bundle upsell",
        "channel": "Email + in-app messaging",
    },
    "At Risk - High Value": {
        "objective": "Reactivate",
        "recommended_action": "Time-boxed win-back incentive",
        "channel": "Email + paid retargeting",
    },
    "Potential Loyalist": {
        "objective": "Grow",
        "recommended_action": "Cross-sell based on recent category history",
        "channel": "Email automation",
    },
    "Promising": {
        "objective": "Nurture",
        "recommended_action": "Second-purchase nudges and social proof",
        "channel": "Email + push",
    },
    "Regular": {
        "objective": "Stabilize",
        "recommended_action": "Cadence reminders and light promotions",
        "channel": "Email automation",
    },
    "Hibernating": {
        "objective": "Selective reactivation",
        "recommended_action": "Low-cost reactivation test, then suppress non-responders",
        "channel": "Email only",
    },
    "New/Low Activity": {
        "objective": "Activate",
        "recommended_action": "Onboarding flow focused on second purchase",
        "channel": "Email + on-site prompts",
    },
}

PRIORITY_SPEND_GUIDANCE = {
    "P1 - Protect": "High budget priority with strict ROI tracking",
    "P2 - Grow": "Medium budget with controlled experimentation",
    "P3 - Maintain": "Low budget, automation-first treatment",
}

EXPECTED_ROI_PROXY = {
    "P1 - Protect": "6-12% incremental return potential",
    "P2 - Grow": "3-8% incremental return potential",
    "P3 - Maintain": "0-3% incremental return potential",
}


def _assign_priority_tier(summary: pd.DataFrame) -> pd.Series:
    """Assign priority tiers by estimated LTV contribution."""
    rank_pct = summary["estimated_ltv_total"].rank(pct=True, ascending=False)
    return pd.cut(
        rank_pct,
        bins=[0.0, 0.34, 0.67, 1.0],
        labels=["P1 - Protect", "P2 - Grow", "P3 - Maintain"],
        include_lowest=True,
    ).astype(str)


def _assign_ltv_signal_tier(summary: pd.DataFrame) -> pd.Series:
    """Classify segment value signal strength by LTV share."""
    share = summary["estimated_ltv_share"]
    return pd.cut(
        share,
        bins=[-0.001, 0.04, 0.15, 1.0],
        labels=["Low", "Medium", "High"],
        include_lowest=True,
    ).astype(str)


def _decision_rule_text(row: pd.Series) -> str:
    signal = row["ltv_signal_tier"]
    objective = row["objective"]
    if signal == "High" and objective in {"Reactivate", "Selective reactivation"}:
        return "High value + weak engagement -> prioritize reactivation"
    if signal == "Medium" and objective == "Reactivate":
        return "Mid-high value + weakening engagement -> run controlled win-back"
    if signal == "High" and objective in {"Retain", "Retain and grow"}:
        return "High value + strong engagement -> invest in retention"
    if signal in {"Low", "Medium"} and objective in {"Activate", "Nurture", "Stabilize", "Grow"}:
        return "Lower value or early lifecycle -> focus on efficient growth"
    return "Run controlled campaign and reassess with new data"


def build_segment_action_plan(
    segment_value_summary: pd.DataFrame,
    segment_col: str = "rule_label",
) -> pd.DataFrame:
    """Build a decision-ready action table from segment value summary."""
    if segment_col not in segment_value_summary.columns:
        raise ValueError(f"Column '{segment_col}' is required for action planning.")
    if "estimated_ltv_total" not in segment_value_summary.columns:
        raise ValueError("Column 'estimated_ltv_total' is required for action planning.")

    out = segment_value_summary.copy()
    out["priority_tier"] = _assign_priority_tier(out)
    out["ltv_signal_tier"] = _assign_ltv_signal_tier(out)

    out["objective"] = out[segment_col].map(
        lambda s: SEGMENT_POLICY.get(s, {}).get("objective", "Monitor")
    )
    out["recommended_action"] = out[segment_col].map(
        lambda s: SEGMENT_POLICY.get(
            s,
            {},
        ).get("recommended_action", "Run small diagnostic campaign and reassess")
    )
    out["channel"] = out[segment_col].map(
        lambda s: SEGMENT_POLICY.get(s, {}).get("channel", "Email automation")
    )
    out["spend_guidance"] = out["priority_tier"].map(PRIORITY_SPEND_GUIDANCE)
    out["expected_roi_proxy"] = out["priority_tier"].map(EXPECTED_ROI_PROXY)
    out["decision_rule"] = out.apply(_decision_rule_text, axis=1)
    return out
