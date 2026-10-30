# Architecture — Enterprise E-Commerce Analytics POC

## Logical design

~~~text
source CSVs -> OneLake Files/source
            -> Data Factory Copy -> OneLake Files/raw
            -> Spark Bronze (preserve raw fields, metadata)
            -> Spark Silver (clean typed data + quality checks)
            -> Spark Gold (star schema + business metrics)
            -> SQL analytics endpoint -> semantic model -> Power BI
~~~

## Source data and keys
- Customers: customer_id; city, signup date.
- Products: product_id; category, price and active flag.
- Orders: order_id and customer_id; order status/date.
- Order items: order_item_id and order_id/product_id; quantity, price, discount.
- Payments: payment_id and order_id; payment status and method.

## Medallion rationale
- **Bronze** records the original source and ingestion timestamp.
- **Silver** enforces types and business rules and checks referential integrity.
- **Gold** separates dimensions and fact tables for analytics.

## Gold grain and metric definitions
- `fact_sales` = exactly one row per **order item**, not per order.
- `gross_amount = quantity * unit_price`.
- `discount_amount = gross_amount * discount_pct / 100`.
- `net_amount = gross_amount - discount_amount`.
- POC-only `recognized_revenue`: net amount for Completed/Shipped orders; zero for Pending/Cancelled. **This is a simplifying demonstration assumption, not financial accounting guidance.**
- Payment data must not be aggregated as order-level amounts after a join to multiple order lines because it risks double-counting.
- Dimensions: `dim_customer`, `dim_product`, `dim_date`; Fact: `fact_sales`.

## Enterprise discussion topics
- Separate Lakehouses and environments vs one Lakehouse in a first POC.
- Idempotent full refresh vs CDC/incremental MERGE.
- Schema drift, duplicates, dead-letter management.
- RBAC, classification, lineage and sensitivity labeling.
- Fabric capacity sizing, operational monitoring and failure recovery.
- Fabric-managed Data Factory vs external orchestration.

No real personal data, secrets or tenant IDs belong in this public repository.
