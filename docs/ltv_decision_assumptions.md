# LTV and Decision Policy Assumptions

## Why this layer exists

RFM segmentation alone does not answer budget allocation.  
This document defines the assumptions used to convert segment labels into expected-value priorities and campaign actions.

## LTV heuristic assumptions

The customer-level expected value uses:

- observed monetary value as the baseline,
- a recency decay term (half-life style),
- a frequency multiplier (log-scaled uplift).

Formula:

`estimated_ltv = Monetary * exp(-ln(2) * Recency / half_life_days) * (1 + log1p(Frequency))`

Interpretation:

- lower recency (more recent purchase) increases estimated near-term value,
- higher frequency increases expected value potential,
- the model is transparent and intentionally simple for operational explainability.

## Decision policy assumptions

1. Segment strategy maps are business defaults, not immutable truths.
2. Priority tiers are assigned by estimated LTV contribution ranking.
3. Spend guidance is proportional to value tier:
   - P1: protect value with higher budget and stricter monitoring,
   - P2: growth-focused experimentation,
   - P3: low-cost automation first.

## Risks and trade-offs

- This approach does not estimate causal uplift.
- Seasonal effects and channel mix changes can shift performance.
- Priority tiers should be recalibrated regularly with fresh data.

## Validation recommendations

- Track conversion and incremental revenue by segment-action pair.
- Run holdout or A/B experiments for each major tactic.
- Reassess thresholds and policy mapping quarterly.
