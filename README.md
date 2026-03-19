# Customer Segmentation and Revenue Optimization with RFM

## Executive Summary

This project turns transaction logs into customer decisions.  
Instead of stopping at segment labels, the pipeline is designed to answer: which customers should be retained, reactivated, upsold, or deprioritized to improve marketing ROI.

The baseline solution combines interpretable RFM segmentation with clustering diagnostics and produces reusable artifacts for downstream decision workflows.

## Business Problem

Lifecycle marketing teams often run broad campaigns with weak prioritization.  
This causes three recurring losses:

- under-investment in high-value customers,
- delayed intervention for at-risk customers,
- wasteful spend on low-probability segments.

The objective of this repository is to provide a practical, transparent segmentation foundation that can be operationalized by CRM and Growth teams.

## Decision Framework

### Segment and action logic

The project uses rule-based labels and clustering outputs to support campaign decisions:

- `High Value` and `Loyal`: retention and VIP benefits to protect long-term value.
- `Potential Loyalist` and `Promising`: upsell/cross-sell to increase basket value.
- `At Risk - High Value`: win-back programs with controlled incentives.
- `New/Low Activity` and `Hibernating`: low-cost activation or selective suppression.

### Why this approach

- RFM provides high interpretability for non-technical stakeholders.
- KMeans and DBSCAN offer complementary structure checks.
- The final segmentation choice favors business actionability, not metric optimization alone.

## Methodology

1. Data loading and cleaning (`src/rfm/data.py`)
   - remove canceled invoices and invalid quantity/price rows,
   - parse timestamps and compute transaction value (`totalcost`).
2. Feature engineering (`src/rfm/features.py`)
   - build `Recency`, `Frequency`, `Monetary` per customer,
   - add quartile scores for explainable ranking.
3. Labeling and clustering
   - rule-based labels (`src/rfm/labels.py`),
   - KMeans/DBSCAN diagnostics (`src/rfm/segmentation.py`).
4. Reproducible run path
   - script entrypoint: `scripts/run_rfm_segmentation.py`.

## Results (Current Baseline Run)

- Customers segmented: **4,338**
- KMeans baseline clusters: **3**
- DBSCAN groups (including noise): **4**
- Largest rule-based segment: **New/Low Activity (1,742 customers)**
- KMeans silhouette peak in search range: **k=2 (0.8958)**, while **k=3** is retained for campaign granularity.

Generated artifacts:

- `outputs/rfm_segmentation.csv`
- `outputs/kmeans_metrics.csv`
- `outputs/kmeans_selection.png`

## Business Recommendations

Recommended baseline actions from current segmentation:

- Protect `High Value` and `Loyal` cohorts with loyalty offers and service quality controls.
- Run targeted reactivation campaigns for `At Risk - High Value` customers.
- Build onboarding and second-purchase journeys for `New/Low Activity`.
- Reduce paid-channel pressure for persistently low-value dormant users.

## Interview Defensibility

This repository is designed to support common hiring-manager questions:

- Why start with RFM instead of direct clustering?
- Why use `k=3` although silhouette peaks at `k=2`?
- How should decisions change for high-frequency but low-monetary users?
- How would you validate segment impact on revenue and retention?

## Repository Structure

```text
.
├── README.md
├── rfm_stock_data.csv
├── outputs/
├── scripts/
│   └── run_rfm_segmentation.py
├── src/
│   └── rfm/
├── tests/
├── rfm_customer_segmentation.ipynb
├── how_to_choose_k.ipynb
└── kmeans_optimization.ipynb
```

