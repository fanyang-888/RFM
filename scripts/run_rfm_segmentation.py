from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from rfm.data import load_transactions
from rfm.features import add_quartile_scores, build_rfm_table
from rfm.labels import add_rule_based_label
from rfm.ltv import estimate_customer_ltv, summarize_ltv_by_segment
from rfm.policy import build_segment_action_plan
from rfm.segmentation import (
    evaluate_kmeans_range,
    evaluate_kmeans_stability,
    fit_dbscan,
    fit_kmeans,
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_path = root / "data" / "raw" / "rfm_stock_data.csv"
    output_dir = root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_transactions(data_path)
    rfm = build_rfm_table(df)
    rfm = add_rule_based_label(rfm)
    rfm = add_quartile_scores(rfm)

    X = rfm[["Recency", "Frequency", "Monetary"]]
    metrics = evaluate_kmeans_range(X, k_min=2, k_max=10)
    stability = evaluate_kmeans_stability(X, k_min=2, k_max=10)
    km_labels, _ = fit_kmeans(X, n_clusters=3)
    db_labels, _ = fit_dbscan(X, eps=0.2, min_samples=5)
    rfm["kmeans_cluster"] = km_labels
    rfm["dbscan_cluster"] = db_labels
    ltv = estimate_customer_ltv(rfm)
    segment_value = summarize_ltv_by_segment(ltv, segment_col="rule_label")
    segment_actions = build_segment_action_plan(segment_value, segment_col="rule_label")

    rfm.to_csv(output_dir / "rfm_segmentation.csv")
    ltv.to_csv(output_dir / "customer_ltv.csv")
    segment_value.to_csv(output_dir / "segment_value_summary.csv", index=False)
    segment_actions.to_csv(output_dir / "segment_action_plan.csv", index=False)
    metrics.to_csv(output_dir / "kmeans_metrics.csv", index=False)
    stability.to_csv(output_dir / "kmeans_stability.csv", index=False)

    fig, axes = plt.subplots(1, 3, figsize=(16, 4))
    axes[0].plot(metrics["k"], metrics["sse"], marker="o")
    axes[0].set_title("Elbow Curve")
    axes[0].set_xlabel("Number of Clusters (k)")
    axes[0].set_ylabel("Sum of Squared Errors (SSE)")

    axes[1].plot(metrics["k"], metrics["silhouette"], marker="o")
    axes[1].set_title("Silhouette Scores")
    axes[1].set_xlabel("Number of Clusters (k)")
    axes[1].set_ylabel("Silhouette Score")

    axes[2].errorbar(
        stability["k"],
        stability["silhouette_mean"],
        yerr=stability["silhouette_std"],
        marker="o",
        capsize=3,
    )
    axes[2].set_title("Silhouette Stability")
    axes[2].set_xlabel("Number of Clusters (k)")
    axes[2].set_ylabel("Mean ± Std")

    fig.tight_layout()
    fig.savefig(output_dir / "kmeans_selection.png", dpi=150)
    plt.close(fig)

    print(f"Saved outputs to: {output_dir}")


if __name__ == "__main__":
    main()

