from __future__ import annotations

import pandas as pd

from rfm.segmentation import evaluate_kmeans_range, evaluate_kmeans_stability, fit_dbscan, fit_kmeans


def _sample_rfm_features() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Recency": [5.0, 7.0, 10.0, 20.0, 35.0, 40.0, 90.0, 110.0, 130.0, 170.0],
            "Frequency": [15.0, 14.0, 11.0, 8.0, 7.0, 6.0, 4.0, 3.0, 2.0, 1.0],
            "Monetary": [900.0, 850.0, 700.0, 420.0, 380.0, 310.0, 210.0, 150.0, 100.0, 60.0],
        }
    )


def test_evaluate_kmeans_range_outputs_extended_metrics() -> None:
    X = _sample_rfm_features()
    out = evaluate_kmeans_range(X, k_min=2, k_max=4, random_state=42)

    expected_cols = {"k", "sse", "silhouette", "calinski_harabasz", "davies_bouldin"}
    assert expected_cols.issubset(out.columns)
    assert out["k"].tolist() == [2, 3, 4]
    assert out["sse"].gt(0).all()
    assert out["silhouette"].between(-1, 1).all()
    assert out["calinski_harabasz"].gt(0).all()
    assert out["davies_bouldin"].gt(0).all()


def test_evaluate_kmeans_stability_outputs_expected_summary() -> None:
    X = _sample_rfm_features()
    out = evaluate_kmeans_stability(X, k_min=2, k_max=4, random_states=(11, 22, 33))

    expected_cols = {
        "k",
        "n_runs",
        "silhouette_mean",
        "silhouette_std",
        "silhouette_min",
        "silhouette_max",
    }
    assert expected_cols.issubset(out.columns)
    assert out["k"].tolist() == [2, 3, 4]
    assert out["n_runs"].eq(3).all()
    assert out["silhouette_std"].ge(0).all()
    assert out["silhouette_mean"].between(-1, 1).all()
    assert out["silhouette_min"].le(out["silhouette_max"]).all()


def test_fit_kmeans_and_dbscan_output_lengths() -> None:
    X = _sample_rfm_features()
    km_labels, _ = fit_kmeans(X, n_clusters=3, random_state=42)
    db_labels, _ = fit_dbscan(X, eps=0.9, min_samples=2)

    assert len(km_labels) == len(X)
    assert len(db_labels) == len(X)
