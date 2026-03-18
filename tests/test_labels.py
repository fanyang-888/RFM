from __future__ import annotations

import pandas as pd

from rfm.labels import add_rule_based_label


def test_rule_based_label_outputs_columns() -> None:
    rfm = pd.DataFrame(
        {
            "Recency": [1.0, 50.0, 120.0, 220.0],
            "Frequency": [20.0, 5.0, 2.0, 1.0],
            "Monetary": [500.0, 120.0, 60.0, 20.0],
        },
        index=[101, 102, 103, 104],
    )
    out = add_rule_based_label(rfm)

    assert "rule_code" in out.columns
    assert "rule_label" in out.columns
    assert out["rule_code"].map(len).eq(3).all()
    assert out["rule_label"].notna().all()

