# Lab 04 — Silver: Orders first

Status: **Hands-on not yet verified**. Complete one entity at a time.

## Concepts
Bronze = raw strings preserved; Silver = validated and typed data. For this first POC, the Silver table is in `lh_ecom_bronze.dbo`, alongside Bronze; production environments commonly separate Bronze/Silver/Gold into independent Lakehouses for isolation and governance.

## Step 1
Create a Fabric notebook: `nb_ecom_02_silver_transformation`. Attach `lh_ecom_bronze` as default lakehouse.

Copy the code from [02a_silver_orders.py](../notebooks/02a_silver_orders.py) into a code cell and run it.

## Verify
- 300 Bronze rows and 300 Silver rows
- No invalid or missing `order_id`
- No duplicates of `order_id`
- Typed `order_date` is a timestamp, not a string
- Valid statuses: Completed, Shipped, Pending, Cancelled
- Delta table `dbo.silver_orders` appears in Tables.

## Self-check
- What happens if source sends `order_date = "not a date"`?
- Why validate before doing `mode("overwrite")`?
- Does `dropDuplicates()` always provide a safe business rule? (No; define precedence when duplicates have different values.)
- How would you preserve failed records in a production quarantine table?
