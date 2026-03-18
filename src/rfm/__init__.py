"""RFM segmentation utilities."""

from .data import load_transactions
from .features import build_rfm_table, add_quartile_scores, zscore_features
from .labels import add_rule_based_label
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
    "evaluate_kmeans_range",
    "fit_kmeans",
    "fit_dbscan",
]

