# RFM Customer Segmentation for Lifecycle Marketing

Production-oriented customer segmentation case study for an e-commerce/retail context.

## Why This Project Matters

Most retail teams can describe customer behavior, but struggle to turn transaction logs into **actionable segment decisions**.
This project demonstrates how to convert raw invoice-level data into customer segments that can support:

- retention prioritization,
- campaign targeting,
- and value-based lifecycle strategy.

## Business Problem

Marketing teams often apply one-size-fits-all campaigns, causing:

- high spend on low-value audiences,
- weak retention treatment for high-risk customers,
- and unclear prioritization between "high value", "at risk", and "new" segments.

## Who Cares

- **Growth/CRM Managers**: need practical audience definitions for campaign execution.
- **Product/Analytics Teams**: need transparent segmentation logic tied to measurable behaviors.
- **Leadership**: need a simple way to prioritize customer cohorts by business impact.

## Business Value Created

- Builds an interpretable RFM segmentation baseline for lifecycle marketing.
- Adds clustering-based segmentation diagnostics (KMeans/DBSCAN) for pattern discovery.
- Produces reusable outputs for downstream campaign planning and experimentation.

## Project Files

- `rfm_customer_segmentation.ipynb`: end-to-end RFM analysis and segmentation notebook
- `how_to_choose_k.ipynb`: K selection notes and experiments
- `kmeans_optimization.ipynb`: KMeans optimization experiments
- `rfm_project_overview.md`: project background and business context
- `K-means.md`: KMeans notes and references
- `rfm_stock_data.csv`: source dataset

## Quick Start

1. Create and activate a Python environment (Python 3.9+ recommended).
2. Install dependencies (example):
   - `pandas`
   - `numpy`
   - `matplotlib`
   - `seaborn`
   - `scikit-learn`
   - `jupyter`
3. Open the notebooks and run cells from top to bottom.

## Data

The project uses `rfm_stock_data.csv` in the repository root.  
No external data download is required for the local workflow after localization updates.

## Notes

- The repository is being upgraded as a hiring-focused portfolio project.
- Small, scoped commits are pushed incrementally to keep changes reviewable.

