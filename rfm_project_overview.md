# Optimizing Retail Customer Relationship Management with a Python-Based RFM Model

[TOC]

## Project Background and Objective

In a competitive online retail market, customer relationship management is critical for sustainable growth.
This project applies an RFM framework to better understand customer behavior and improve segmentation quality.

Main objectives:

1. Calculate RFM indicators with Python:
   - Recency (how recently the customer purchased)
   - Frequency (how often the customer purchased)
   - Monetary (how much the customer spent)
2. Build customer segments using both rule-based RFM scoring and clustering methods (KMeans/DBSCAN).
3. Support targeted marketing, personalization, and resource prioritization.

## Business Value

1. **Personalization**: provide more relevant product recommendations by segment.
2. **Targeted marketing**: design higher-conversion campaigns using segment behavior patterns.
3. **Resource efficiency**: prioritize high-value and high-potential customer groups.

## Dataset

### Description

The dataset contains all transactions from a UK-based online retailer between 2010-12-01 and 2011-12-09.
The company mainly sells unique gift items, and many customers are wholesalers.

### Fields

1. **InvoiceNo**: transaction ID (if it starts with `C`, the transaction is canceled)
2. **StockCode**: product/item code
3. **Description**: product description
4. **Quantity**: number of units in the transaction
5. **InvoiceDate**: transaction timestamp
6. **UnitPrice**: unit price in GBP
7. **CustomerID**: unique customer ID
8. **Country**: customer country

## What is RFM?

RFM is a customer value analysis framework based on three dimensions:

- **R (Recency)**: time since the most recent purchase
- **F (Frequency)**: number of purchases in a period
- **M (Monetary)**: total spending in a period

RFM analysis helps convert transaction history into actionable customer segments.

![](https://image.woshipm.com/wp-files/2023/03/IT8NGS7FM3p418AgHzgh.png)

## What is KMeans Clustering?

<iframe width="853" height="480" src="https://www.youtube.com/embed/4b5d3muPQmA" title="StatQuest: K-means clustering" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

KMeans partitions samples into `K` groups by minimizing within-cluster distance.
Each sample belongs to exactly one cluster, so it is a hard-clustering algorithm.

## DBSCAN

<iframe width="853" height="480" src="https://www.youtube.com/embed/RDZUdRSDOok" title="Clustering with DBSCAN, Clearly Explained!!!" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

