"""RFM segmentation utilities."""

from .data import load_transactions
from .features import build_rfm_table, add_quartile_scores, zscore_features
from .labels import add_rule_based_label
from .ltv import estimate_customer_ltv, summarize_ltv_by_segment
from .segmentation import (
    evaluate_kmeans_range,
    fit_kmeans,
    fit_dbscan,
)

__all__ = [
    "load_transactions",
    "build_rfm_table",
    "add_quartile_scores",
    "zscore_features",
    "add_rule_based_label",
    "estimate_customer_ltv",
    "summarize_ltv_by_segment",
    "evaluate_kmeans_range",
    "fit_kmeans",
    "fit_dbscan",
]

