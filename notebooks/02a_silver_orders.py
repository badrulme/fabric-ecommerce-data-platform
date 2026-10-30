# Fabric notebook cell: Silver orders (first Silver lab).
# Prerequisite: dbo.bronze_orders exists and lh_ecom_bronze is the default lakehouse.
from pyspark.sql import functions as F

bronze_orders = spark.table("dbo.bronze_orders")
print("Bronze rows:", bronze_orders.count())

silver_orders = (
    bronze_orders
    .select("order_id", "customer_id", "order_date", "order_status", "currency")
    .withColumn("order_id", F.trim(F.col("order_id")))
    .withColumn("customer_id", F.trim(F.col("customer_id")))
    .withColumn("order_status", F.trim(F.col("order_status")))
    .withColumn("currency", F.upper(F.trim(F.col("currency"))))
    .withColumn("order_date", F.to_timestamp(
        F.col("order_date"), "yyyy-MM-dd HH:mm:ss"))
)

missing_keys = silver_orders.filter(
    F.col("order_id").isNull() | (F.col("order_id") == "")
).count()
duplicate_keys = silver_orders.groupBy("order_id").count().filter(
    F.col("count") > 1
).count()
invalid_dates = silver_orders.filter(F.col("order_date").isNull()).count()
invalid_statuses = silver_orders.filter(
    ~F.col("order_status").isin("Completed", "Shipped", "Pending", "Cancelled")
    | F.col("order_status").isNull()
).count()

print("Missing order IDs:", missing_keys)
print("Duplicate order IDs:", duplicate_keys)
print("Invalid order dates:", invalid_dates)
print("Invalid statuses:", invalid_statuses)

assert missing_keys == 0, "Null/empty order_id detected"
assert duplicate_keys == 0, "Duplicate order_id detected"
assert invalid_dates == 0, "Invalid order_date detected"
assert invalid_statuses == 0, "Unexpected order_status detected"
assert silver_orders.count() == 300, "Unexpected row count"

(silver_orders.write.format("delta").mode("overwrite")
 .option("overwriteSchema", "true").saveAsTable("dbo.silver_orders"))

print("Silver rows:", spark.table("dbo.silver_orders").count())
spark.table("dbo.silver_orders").printSchema()
display(spark.table("dbo.silver_orders").limit(5))
