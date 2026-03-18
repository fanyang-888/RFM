from __future__ import annotations

import pandas as pd
from sklearn.preprocessing import StandardScaler


RFM_COLUMNS = ["Recency", "Frequency", "Monetary"]


def build_rfm_table(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate transaction rows to per-customer RFM table."""
    rfm = df.pivot_table(
        index="CustomerID",
        values=["InvoiceNo", "totalcost", "InvoiceDate"],
        aggfunc={"InvoiceNo": pd.Series.nunique, "totalcost": "sum", "InvoiceDate": "max"},
    ).rename(columns={"InvoiceNo": "Frequency", "totalcost": "Monetary", "InvoiceDate": "LastInvoiceDate"})
    rfm["Recency"] = (rfm["LastInvoiceDate"].max() - rfm["LastInvoiceDate"]).dt.days.astype(float)
    return rfm


def zscore_features(rfm: pd.DataFrame) -> pd.DataFrame:
    """Return z-scored R, F, M features."""
    scaler = StandardScaler()
    z = scaler.fit_transform(rfm[RFM_COLUMNS])
    return pd.DataFrame(z, index=rfm.index, columns=RFM_COLUMNS)


def add_quartile_scores(rfm: pd.DataFrame) -> pd.DataFrame:
    """Add quartile-based RFM scores and combined score string."""
    out = rfm.copy()
    quantile = out[RFM_COLUMNS].quantile(q=[0.25, 0.5, 0.75])

    def r_score(value: float) -> int:
        if value <= quantile.loc[0.25, "Recency"]:
            return 1
        if value <= quantile.loc[0.50, "Recency"]:
            return 2
        if value <= quantile.loc[0.75, "Recency"]:
            return 3
        return 4

    def fm_score(value: float, col: str) -> int:
        if value <= quantile.loc[0.25, col]:
            return 4
        if value <= quantile.loc[0.50, col]:
            return 3
        if value <= quantile.loc[0.75, col]:
            return 2
        return 1

    out["R_Quartile"] = out["Recency"].apply(r_score)
    out["F_Quartile"] = out["Frequency"].apply(lambda x: fm_score(x, "Frequency"))
    out["M_Quartile"] = out["Monetary"].apply(lambda x: fm_score(x, "Monetary"))
    out["RFMScore"] = (
        out["R_Quartile"].astype(str)
        + out["F_Quartile"].astype(str)
        + out["M_Quartile"].astype(str)
    )
    out["TotalScore"] = out["R_Quartile"] + out["F_Quartile"] + out["M_Quartile"]
    return out

