# Fabric Notebook 03 — Gold. Attach lh_ecom_bronze as DEFAULT Lakehouse.
from pyspark.sql import functions as F
from pyspark.sql import types as T

MONEY = T.DecimalType(18, 2)
customers = spark.table("silver_customers")
products = spark.table("silver_products")
orders = spark.table("silver_orders")
items = spark.table("silver_order_items")
payments = spark.table("silver_payments")

dim_customer = customers.select(
    F.sha2("customer_id", 256).alias("customer_key"),
    "customer_id", "customer_name", "city", "country", "signup_date")
dim_product = products.select(
    F.sha2("product_id", 256).alias("product_key"),
    "product_id", "product_name", "category", "is_active")
dim_date = (orders.select(F.to_date("order_date").alias("full_date")).distinct()
    .withColumn("date_key", F.date_format("full_date", "yyyyMMdd").cast("int"))
    .withColumn("calendar_year", F.year("full_date"))
    .withColumn("calendar_month", F.month("full_date"))
    .withColumn("day_of_month", F.dayofmonth("full_date")))

joined = (items.alias("i")
    .join(orders.alias("o"), F.col("i.order_id") == F.col("o.order_id"), "inner")
    .join(payments.alias("p"), F.col("i.order_id") == F.col("p.order_id"), "left"))

gross = (F.col("i.quantity") * F.col("i.unit_price")).cast(MONEY)
discount = (gross * F.col("i.discount_pct") / F.lit(100)).cast(MONEY)
net = (gross - discount).cast(MONEY)

fact_sales = joined.select(
    F.col("i.order_item_id"), F.col("i.order_id"),
    F.sha2(F.col("o.customer_id"), 256).alias("customer_key"),
    F.sha2(F.col("i.product_id"), 256).alias("product_key"),
    F.date_format(F.col("o.order_date"), "yyyyMMdd").cast("int").alias("date_key"),
    F.col("o.order_status"), F.col("o.currency"),
    F.col("p.payment_method"), F.col("p.payment_status"), F.col("i.quantity"),
    gross.alias("gross_amount"), discount.alias("discount_amount"),
    net.alias("net_amount"),
    F.when(F.col("o.order_status").isin("Completed", "Shipped"), net)
     .otherwise(F.lit(0).cast(MONEY)).alias("recognized_revenue"))

assert fact_sales.count() == items.count(), "Fact table has incorrect grain"
assert fact_sales.join(dim_customer, "customer_key", "left_anti").count() == 0
assert fact_sales.join(dim_product, "product_key", "left_anti").count() == 0
assert fact_sales.join(dim_date, "date_key", "left_anti").count() == 0

for name, df in [("dim_customer", dim_customer), ("dim_product", dim_product),
                 ("dim_date", dim_date), ("fact_sales", fact_sales)]:
    df.write.format("delta").mode("overwrite").option(
        "overwriteSchema", "true").saveAsTable(name)
    print(f"{name}: {df.count()} records")

spark.sql("""SELECT order_status, COUNT(*) AS lines,
                   ROUND(SUM(recognized_revenue), 2) AS recognized_revenue
              FROM fact_sales GROUP BY order_status ORDER BY order_status""").show(truncate=False)
