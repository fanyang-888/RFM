from __future__ import annotations

import pandas as pd

from rfm.features import add_quartile_scores, build_rfm_table


def _sample_transactions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CustomerID": [1, 1, 2, 2, 2, 3],
            "InvoiceNo": ["A1", "A2", "B1", "B2", "B3", "C1"],
            "InvoiceDate": pd.to_datetime(
                [
                    "2011-01-01",
                    "2011-01-10",
                    "2011-01-03",
                    "2011-01-08",
                    "2011-01-20",
                    "2011-01-15",
                ]
            ),
            "totalcost": [10.0, 20.0, 5.0, 5.0, 10.0, 7.5],
        }
    )


def test_build_rfm_table_basic_aggregation() -> None:
    df = _sample_transactions()
    rfm = build_rfm_table(df)

    assert set(rfm.columns) == {"Frequency", "Monetary", "LastInvoiceDate", "Recency"}
    assert int(rfm.loc[1, "Frequency"]) == 2
    assert float(rfm.loc[1, "Monetary"]) == 30.0
    assert int(rfm.loc[2, "Frequency"]) == 3
    assert float(rfm.loc[2, "Monetary"]) == 20.0


def test_add_quartile_scores_adds_expected_columns() -> None:
    df = _sample_transactions()
    rfm = build_rfm_table(df)
    scored = add_quartile_scores(rfm)

    expected = {"R_Quartile", "F_Quartile", "M_Quartile", "RFMScore", "TotalScore"}
    assert expected.issubset(set(scored.columns))
    assert scored["RFMScore"].map(len).eq(3).all()
    assert scored["TotalScore"].between(3, 12).all()

