from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_transactions(csv_path: str | Path, encoding: str = "ISO-8859-1") -> pd.DataFrame:
    """Load and clean raw retail transactions."""
    df = pd.read_csv(csv_path, encoding=encoding)
    df = df.dropna(subset=["CustomerID", "InvoiceDate", "Quantity", "UnitPrice"]).copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%m/%d/%Y %H:%M")
    df["CustomerID"] = df["CustomerID"].astype(int)
    # Remove canceled invoices and invalid rows.
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()
    df["totalcost"] = df["Quantity"] * df["UnitPrice"]
    return df

