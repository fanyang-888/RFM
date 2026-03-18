from __future__ import annotations

import pandas as pd


RULE_LABEL_MAP = {
    "011": "High Value",
    "111": "Loyal",
    "001": "At Risk - High Value",
    "101": "Promising",
    "110": "Potential Loyalist",
    "010": "Regular",
    "100": "Hibernating",
    "000": "New/Low Activity",
}


def add_rule_based_label(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Add an English rule-based segment label using z-score sign of R/F/M.
    """
    out = rfm.copy()
    z = out[["Recency", "Frequency", "Monetary"]].apply(lambda s: (s - s.mean()) / s.std())
    code = (
        (z["Recency"] > 0).astype(int).astype(str)
        + (z["Frequency"] > 0).astype(int).astype(str)
        + (z["Monetary"] > 0).astype(int).astype(str)
    )
    out["rule_code"] = code
    out["rule_label"] = out["rule_code"].map(RULE_LABEL_MAP).fillna("Unknown")
    return out

