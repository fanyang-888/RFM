# RFM Segmentation Dashboard Specification

## Objective

Provide a decision dashboard that translates segmentation outputs into daily/weekly CRM actions, budget priorities, and performance tracking.

## Target Users

- CRM manager: decide retention/reactivation priorities.
- Growth analyst (DA): monitor segment mix and campaign opportunity.
- Data scientist (DS): validate segment stability and value concentration.

## Data Inputs

- `outputs/rfm_segmentation.csv`
- `outputs/customer_ltv.csv`
- `outputs/segment_value_summary.csv`
- `outputs/segment_action_plan.csv`
- `outputs/kmeans_metrics.csv`
- `outputs/kmeans_stability.csv`
- Optional warehouse view: `sql/rfm_segment_snapshot.sql`

## Recommended Pages and Visuals

## Page 1: Executive Snapshot

- KPI cards:
  - total customers
  - total observed monetary value
  - total estimated LTV
  - share of top 20% customers (revenue and LTV)
- Chart: segment distribution by customer count (`rule_label`).
- Chart: segment contribution by estimated LTV share (`estimated_ltv_share`).

Business question: Where is value concentrated right now?

## Page 2: Priority and Action Plan

- Table: `rule_label`, `priority_tier`, `objective`, `recommended_action`, `channel`, `expected_roi_proxy`.
- Stacked bar: customer volume split by `priority_tier`.
- Funnel/ordered bar: P1 -> P2 -> P3 value share.

Business question: Which segments get budget first and why?

## Page 3: Validation and Stability

- Line chart: `k` vs `sse`, `silhouette`, `calinski_harabasz`, `davies_bouldin`.
- Errorbar or band chart: `silhouette_mean` with `silhouette_std` by `k`.
- Table: stability summary (`k`, `silhouette_mean`, `silhouette_std`, `silhouette_min`, `silhouette_max`).

Business question: Is the selected segmentation stable enough for operations?

## Key Metrics Dictionary

- `estimated_ltv`: heuristic customer value score from Monetary x recency weight x frequency multiplier.
- `estimated_ltv_share`: segment contribution to total estimated LTV.
- `priority_tier`:
  - `P1 - Protect`
  - `P2 - Grow`
  - `P3 - Maintain`
- `expected_roi_proxy`: planning proxy for spend prioritization, not causal uplift.

## Refresh and Governance

- Refresh cadence: weekly for planning, daily for campaign execution if pipeline supports it.
- Data quality checks:
  - non-null `CustomerID`
  - positive `Quantity` and `UnitPrice`
  - no canceled invoices (`InvoiceNo` starts with `C`)
- Ownership:
  - DA owns dashboard reliability and metric definitions.
  - DS owns segmentation method updates and validation diagnostics.
  - CRM/Growth owns campaign execution and experiment feedback.
