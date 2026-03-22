from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler


def evaluate_kmeans_range(
    X: pd.DataFrame,
    k_min: int = 2,
    k_max: int = 10,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Compute clustering diagnostics for a range of k values.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    rows: list[dict[str, float]] = []
    for k in range(k_min, k_max + 1):
        model = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = model.fit_predict(X_scaled)
        sse = float(model.inertia_)
        sil = float(silhouette_score(X_scaled, labels))
        ch = float(calinski_harabasz_score(X_scaled, labels))
        dbi = float(davies_bouldin_score(X_scaled, labels))
        rows.append(
            {
                "k": k,
                "sse": sse,
                "silhouette": sil,
                "calinski_harabasz": ch,
                "davies_bouldin": dbi,
            }
        )
    return pd.DataFrame(rows)


def evaluate_kmeans_stability(
    X: pd.DataFrame,
    k_min: int = 2,
    k_max: int = 10,
    random_states: tuple[int, ...] = (7, 13, 29, 42, 77),
) -> pd.DataFrame:
    """
    Evaluate silhouette stability across random seeds for each k.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    rows: list[dict[str, float]] = []
    for k in range(k_min, k_max + 1):
        silhouette_values: list[float] = []
        for seed in random_states:
            model = KMeans(n_clusters=k, random_state=seed, n_init=10)
            labels = model.fit_predict(X_scaled)
            silhouette_values.append(float(silhouette_score(X_scaled, labels)))

        sil_arr = np.array(silhouette_values, dtype=float)
        rows.append(
            {
                "k": k,
                "n_runs": len(silhouette_values),
                "silhouette_mean": float(sil_arr.mean()),
                "silhouette_std": float(sil_arr.std(ddof=0)),
                "silhouette_min": float(sil_arr.min()),
                "silhouette_max": float(sil_arr.max()),
            }
        )

    return pd.DataFrame(rows)


def fit_kmeans(
    X: pd.DataFrame, n_clusters: int = 3, random_state: int = 42
) -> tuple[np.ndarray, KMeans]:
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    labels = model.fit_predict(X_scaled)
    return labels, model


def fit_dbscan(
    X: pd.DataFrame, eps: float = 0.2, min_samples: int = 5
) -> tuple[np.ndarray, DBSCAN]:
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(X_scaled)
    return labels, model

