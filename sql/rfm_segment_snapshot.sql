-- RFM Segment Snapshot
-- Purpose: build a DA-friendly customer-level table for segmentation monitoring.
-- Source table assumption: sales_data(CustomerID, InvoiceNo, InvoiceDate, Quantity, UnitPrice)
-- Time window: 2010-12-01 to 2011-12-09 (aligned with project README).

WITH cleaned AS (
    SELECT
        CustomerID,
        InvoiceNo,
        DATE(InvoiceDate) AS InvoiceDate,
        Quantity,
        UnitPrice,
        Quantity * UnitPrice AS total_cost
    FROM sales_data
    WHERE CustomerID IS NOT NULL
      AND Quantity > 0
      AND UnitPrice > 0
      AND InvoiceNo NOT LIKE 'C%'
      AND DATE(InvoiceDate) BETWEEN DATE('2010-12-01') AND DATE('2011-12-09')
),
max_date AS (
    SELECT MAX(InvoiceDate) AS max_invoice_date
    FROM cleaned
),
rfm_base AS (
    SELECT
        c.CustomerID,
        CAST((JULIANDAY(m.max_invoice_date) - JULIANDAY(MAX(c.InvoiceDate))) AS INTEGER) AS Recency,
        COUNT(DISTINCT c.InvoiceNo) AS Frequency,
        ROUND(SUM(c.total_cost), 2) AS Monetary
    FROM cleaned c
    CROSS JOIN max_date m
    GROUP BY c.CustomerID, m.max_invoice_date
),
rfm_scored AS (
    SELECT
        CustomerID,
        Recency,
        Frequency,
        Monetary,
        NTILE(4) OVER (ORDER BY Recency ASC) AS R_Quartile,
        NTILE(4) OVER (ORDER BY Frequency DESC) AS F_Quartile,
        NTILE(4) OVER (ORDER BY Monetary DESC) AS M_Quartile
    FROM rfm_base
),
segment_labeled AS (
    SELECT
        *,
        CAST(R_Quartile AS TEXT) || CAST(F_Quartile AS TEXT) || CAST(M_Quartile AS TEXT) AS rule_code,
        CASE
            WHEN R_Quartile <= 2 AND F_Quartile <= 2 AND M_Quartile <= 2 THEN 'High Value'
            WHEN R_Quartile <= 2 AND F_Quartile <= 2 THEN 'Loyal'
            WHEN R_Quartile >= 3 AND F_Quartile <= 2 AND M_Quartile <= 2 THEN 'At Risk - High Value'
            WHEN R_Quartile <= 2 AND F_Quartile >= 3 THEN 'Regular'
            WHEN R_Quartile >= 3 AND F_Quartile >= 3 AND M_Quartile >= 3 THEN 'Hibernating'
            WHEN R_Quartile <= 2 AND F_Quartile >= 2 AND M_Quartile >= 2 THEN 'Potential Loyalist'
            WHEN R_Quartile >= 3 AND F_Quartile <= 3 AND M_Quartile <= 3 THEN 'Promising'
            ELSE 'New/Low Activity'
        END AS rule_label
    FROM rfm_scored
)
SELECT
    CustomerID,
    Recency,
    Frequency,
    Monetary,
    R_Quartile,
    F_Quartile,
    M_Quartile,
    rule_code,
    rule_label
FROM segment_labeled
ORDER BY CustomerID;
