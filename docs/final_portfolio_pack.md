# Final Portfolio Pack

## Resume Bullet Options

### DS-Oriented Bullets

1. Built an interpretable customer segmentation workflow on UK retail transactions (4,338 customers) using RFM features, rule-based lifecycle labels, and KMeans/DBSCAN diagnostics to balance operational explainability with structure validation.
2. Strengthened validation with segment summary integrity checks, concentration analysis diagnostics (top-20% revenue/LTV contribution), and explicit reasoning for choosing an operational `k=3` baseline despite a higher `k=2` silhouette.
3. Packaged the analysis into reproducible modules and scripted execution (`src/` + `scripts/`) with test coverage for feature, labeling, segmentation, and decision-policy contracts.

### DA-Oriented Bullets

1. Converted transaction-level data into decision-ready segment outputs and priority tiers (2 P1 / 3 P2 / 3 P3) that map directly to retain/reactivate/grow campaign actions.
2. Added SQL and stakeholder-delivery artifacts by shipping `sql/rfm_segment_snapshot.sql` for customer-level aggregation and `docs/dashboard_spec.md` for KPI/page ownership handoff.
3. Produced reusable outputs for downstream analytics (`rfm_segmentation`, `segment_value_summary`, `segment_action_plan`) to support budget prioritization and CRM execution planning.

## Likely Interview Questions and Answer Outlines

### 1) Why did you choose RFM as the core representation?
- RFM is interpretable and operationally practical for CRM teams.
- It maps directly to common lifecycle actions (retain, reactivate, grow).
- Strong baseline before moving to higher-complexity embeddings.

### 2) Why use both rule-based segmentation and clustering?
- Rule-based labels provide consistency and explainability.
- Clustering provides exploratory structure and sanity checks.
- Together they balance governance and discovery.

### 3) Your silhouette is best at k=2. Why use k=3 as baseline?
- k=2 is statistically stronger on separation, but less actionable for campaign design.
- k=3 provides practical treatment granularity while remaining interpretable.
- Final choice was made as a business + technical trade-off.

### 4) What are the biggest limitations of this project?
- No direct A/B uplift linkage to campaign outcomes yet.
- No temporal stability validation across rolling windows.
- Segment effectiveness is inferred, not experimentally confirmed.

### 5) How would you validate segment business value next?
- Define segment-level KPI framework (retention rate, repeat order rate, ARPU trend).
- Run holdout or A/B tests on treatment strategies by segment.
- Compare lift versus non-segmented baseline campaigns.

### 6) Why include DBSCAN if KMeans already works?
- DBSCAN tests density-separated structure and identifies noise/outliers.
- It helps avoid overconfidence in centroid-only assumptions.
- Useful as an exploratory robustness check.

### 7) What engineering decisions improved maintainability?
- Split logic into dedicated modules (`data`, `features`, `labels`, `segmentation`).
- Added scripted execution for deterministic artifact generation.
- Added baseline tests for core transformation and label outputs.

### 8) How would this move toward production?
- Add scheduled batch pipeline and data quality checks.
- Add versioned model/segment definitions and monitoring.
- Integrate outputs with CRM activation platform and experiment tracker.

## Role Signal Assessment

This project now most strongly signals:

- Entry-level Data Analyst / Product Analyst (with experimentation mindset)
- Junior Data Scientist (customer analytics / segmentation use cases)
- Analytics Engineer (early-career, Python-based pipeline + reproducibility focus)

Why it is stronger than before:

- Clear business framing and stakeholder relevance
- Explicit methodological reasoning and trade-off logic
- Reproducible pipeline outputs + basic tests
- Interview-defensible narrative beyond notebook exploration

