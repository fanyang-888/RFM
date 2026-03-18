from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def evaluate_kmeans_range(
    X: pd.DataFrame,
    k_min: int = 2,
    k_max: int = 10,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Compute SSE and silhouette score for a range of k values.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    rows: list[dict[str, float]] = []
    for k in range(k_min, k_max + 1):
        model = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = model.fit_predict(X_scaled)
        sse = float(model.inertia_)
        sil = float(silhouette_score(X_scaled, labels))
        rows.append({"k": k, "sse": sse, "silhouette": sil})
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

