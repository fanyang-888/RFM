# Phase 3 - Technical Depth Upgrade Notes

## What Was Added

This phase strengthens the project's methodological credibility by explicitly documenting:

1. why each segmentation method is used,
2. why metric values are interpreted with business context,
3. why the baseline cluster count is a trade-off decision rather than a single-metric optimum.

## Method Justification

### RFM as Primary Representation

- RFM aligns with common lifecycle marketing logic.
- It is transparent for non-technical stakeholders.
- It can be implemented in downstream CRM pipelines without complex feature stores.

### KMeans as Baseline

- Fast and scalable for customer-level segmentation tasks.
- Produces centroids that can be profiled and explained.
- Useful as a first-pass segmentation benchmark before more complex models.

### DBSCAN as Complement

- Helpful for checking non-spherical or density-separated structure.
- Can identify noise points that centroid methods may force into clusters.
- Adds robustness to exploratory segmentation analysis.

## Metric Interpretation Policy

- **SSE** is used to track compactness and elbow behavior.
- **Silhouette** is used to evaluate cluster separability.
- Final choice is constrained by campaign usability and interpretability, not metric rank alone.

## Current Gaps and Exact Next Additions

1. **Stability testing**
   - Add rolling time-window segmentation and compare segment consistency.
2. **DBSCAN sensitivity**
   - Add grid search over `eps` and `min_samples` with summary table.
3. **Outcome linkage**
   - Add segment-level KPI proxy analysis (repeat purchase rate, revenue share).
4. **Validation**
   - Add lightweight tests for feature generation and segmentation outputs.

