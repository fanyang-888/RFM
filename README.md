# RFM Customer Segmentation for Lifecycle Marketing

## Executive Summary

This project transforms retail transaction logs into actionable customer segments using RFM (Recency, Frequency, Monetary) and clustering diagnostics (KMeans, DBSCAN).  
It is designed as a practical baseline for lifecycle marketing decisions such as retention prioritization, win-back targeting, and high-value cohort management.

## Business Problem

Retail teams often run broad campaigns without clear audience prioritization.  
As a result, high-value and high-risk customers may receive the wrong treatment while spend is wasted on low-impact segments.

## Objective / Hypothesis

**Objective:** Build an interpretable segmentation framework from transaction data that can be used by CRM/Growth teams.  
**Hypothesis:** RFM-based cohorts, supported by unsupervised clustering diagnostics, can reveal distinct customer behavior groups and improve campaign planning quality.

## Dataset

- Source file: `rfm_stock_data.csv`
- Granularity: transaction-level records
- Key fields: `InvoiceNo`, `InvoiceDate`, `Quantity`, `UnitPrice`, `CustomerID`, `Country`
- Domain context: UK online retail transactions

## Methodology

1. **Data preparation**
   - Remove canceled invoices and invalid quantity/price rows
   - Parse timestamp fields and derive `totalcost`
2. **RFM feature engineering**
   - `Recency`: days since last purchase
   - `Frequency`: distinct invoice count per customer
   - `Monetary`: total spend per customer
3. **Segmentation approaches**
   - Rule-based segment labels from normalized R/F/M behavior
   - KMeans clustering with k-range diagnostics
   - DBSCAN clustering as a density-based comparison

## Technical Approach

- Modular pipeline in `src/rfm/`:
  - `data.py`: loading + cleaning
  - `features.py`: RFM feature construction and quartile scoring
  - `labels.py`: rule-based segment mapping
  - `segmentation.py`: KMeans/DBSCAN and cluster diagnostics
- Reproducible runner:
  - `scripts/run_rfm_segmentation.py`
- Notebook artifacts:
  - `rfm_customer_segmentation.ipynb`
  - `how_to_choose_k.ipynb`
  - `kmeans_optimization.ipynb`

## Method Choice Rationale

- **Why RFM first:** RFM provides high interpretability for business stakeholders and is easy to operationalize in CRM tooling.
- **Why KMeans:** efficient baseline for compact, centroid-based customer groups and straightforward to explain.
- **Why DBSCAN comparison:** tests whether density-based structure exists and helps detect noise/outlier-heavy cohorts.
- **Why rule-based labels + clustering:** rule-based segments improve explainability; clustering adds pattern discovery and sanity-checking.
- **Why keep `k=3` baseline despite stronger silhouette at `k=2`:** `k=3` offers better campaign action granularity (e.g., retain / grow / reactivate) while staying operationally simple.

## Experiment Design Notes

- KMeans search over `k=2..10` with fixed random state.
- Standardization is applied before clustering to prevent feature-scale dominance.
- Metrics are interpreted jointly:
  - SSE trend checks diminishing returns.
  - Silhouette checks cluster separability.
- Final segmenting decision is not metric-only; it is made with business actionability in mind.

## Evaluation Metrics

For KMeans model selection:

- **SSE (Elbow Curve)** for compactness trend
- **Silhouette Score** for cluster separation quality

Current run output (`outputs/kmeans_metrics.csv`) includes `k=2..10` with both metrics.

Metric caveat:

- High silhouette does not automatically mean best business segmentation.
- A production choice should balance statistical fit, interpretability, and operational usefulness.

## Results

From the latest generated metrics:

- Best silhouette score appears at `k=2` (`0.8958`)
- Operational baseline in pipeline uses `k=3` for more granular segmentation
- Output artifacts generated:
  - `outputs/kmeans_metrics.csv`
  - `outputs/kmeans_selection.png`
  - `outputs/rfm_segmentation.csv`

## Business Insights / Recommendations

- Use segment-based treatment strategy instead of one-size-fits-all campaigns.
- Prioritize retention budgets on high-value but declining-frequency cohorts.
- Create separate onboarding and activation flows for low-activity/new cohorts.
- Use clustering diagnostics as a decision aid, not as the only segmentation authority.

## Limitations

- No A/B test or campaign uplift measurement is included yet.
- Segment business impact is not tied to downstream revenue experiments in this repository.
- Data represents one retail context; generalization across industries is not guaranteed.
- Cluster stability across time windows is not yet evaluated.
- Sensitivity analysis for DBSCAN parameters (`eps`, `min_samples`) is not yet formalized.

## Future Improvements

- Add uplift evaluation framework (e.g., retention or conversion lift by segment).
- Compare additional algorithms (e.g., GMM, HDBSCAN) with explicit trade-off criteria.
- Add lightweight tests and data quality checks for production-readiness.
- Package as a simple API or scheduled batch job for deployment simulation.

## Repository Structure

```text
.
├── README.md
├── rfm_stock_data.csv
├── outputs/
│   ├── kmeans_metrics.csv
│   ├── kmeans_selection.png
│   └── rfm_segmentation.csv
├── scripts/
│   └── run_rfm_segmentation.py
├── src/
│   └── rfm/
│       ├── __init__.py
│       ├── data.py
│       ├── features.py
│       ├── labels.py
│       └── segmentation.py
├── rfm_customer_segmentation.ipynb
├── how_to_choose_k.ipynb
└── kmeans_optimization.ipynb
```

## How to Reproduce

1. Create environment (Python 3.10+ recommended).
2. Install dependencies:
   - `pandas`
   - `numpy`
   - `matplotlib`
   - `scikit-learn`
   - `jupyter`
3. Run pipeline:
   - PowerShell:
     - `$env:PYTHONPATH="src"`
     - `python scripts/run_rfm_segmentation.py`
4. (Optional) Re-run notebooks:
   - `python -m jupyter nbconvert --to notebook --execute --inplace rfm_customer_segmentation.ipynb`
   - `python -m jupyter nbconvert --to notebook --execute --inplace how_to_choose_k.ipynb`
   - `python -m jupyter nbconvert --to notebook --execute --inplace kmeans_optimization.ipynb`

