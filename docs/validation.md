# Validation checklist

## Local
~~~sh
python scripts/generate_data.py --output data/generated --seed 42
python -m unittest discover -s tests -v
~~~

Expected source row counts: customers **120**, products **50**, orders **300**, order_items **600**, payments **300**.

## Fabric after Bronze / Silver / Gold
Execute these SQL statements in the Lakehouse SQL analytics endpoint after the notebooks successfully complete:

~~~sql
SELECT COUNT(*) AS order_count FROM bronze_orders;
SELECT COUNT(*) AS order_count FROM silver_orders;
SELECT COUNT(*) AS sales_lines FROM fact_sales;

SELECT order_status, COUNT(*) AS line_count,
       ROUND(SUM(recognized_revenue), 2) AS revenue
FROM fact_sales
GROUP BY order_status;

SELECT COUNT(*) AS missing_customer_keys
FROM fact_sales f LEFT JOIN dim_customer c
  ON f.customer_key = c.customer_key
WHERE c.customer_key IS NULL;
~~~

Expected: **300 orders**, **600 fact rows**, **0 missing customer keys**. Completed/Shipped revenue should be positive; Pending/Cancelled recognized revenue is zero under the POC assumption.

## Evidence collection
- [ ] Screenshot: Fabric workspace and Lakehouse Files/Tables
- [ ] Screenshot: 5 CSVs in source and raw folders
- [ ] Screenshot: Data Factory pipeline run success and statistics
- [ ] Screenshots: Bronze/Silver/Gold table counts
- [ ] Screenshots: SQL checks and Power BI report
- [ ] Re-run jobs and verify no duplicated fact rows
