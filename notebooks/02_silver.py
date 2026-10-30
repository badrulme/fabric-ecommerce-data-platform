# Fabric Notebook 02 — Silver. Attach lh_ecom_bronze as DEFAULT Lakehouse.
from pyspark.sql import functions as F
from pyspark.sql import types as T

MONEY = T.DecimalType(18, 2)


def clean_strings(df):
    for field in df.schema.fields:
        if isinstance(field.dataType, T.StringType):
            df = df.withColumn(field.name, F.trim(F.col(field.name)))
    return df


def check_primary_key(df, col):
    assert df.filter(F.col(col).isNull() | (F.col(col) == "")).count() == 0, f"Missing {col}"
    assert df.groupBy(col).count().filter("count > 1").count() == 0, f"Duplicate {col}"


customers = clean_strings(spark.table("bronze_customers")).select(
    "customer_id", "customer_name", "email", "city", "country", "signup_date"
).withColumn("signup_date", F.to_date("signup_date", "yyyy-MM-dd"))

products = clean_strings(spark.table("bronze_products")).select(
    "product_id", "product_name", "category", "unit_price", "is_active"
).withColumn("unit_price", F.col("unit_price").cast(MONEY)
).withColumn("is_active", F.col("is_active").cast("boolean"))

orders = clean_strings(spark.table("bronze_orders")).select(
    "order_id", "customer_id", "order_date", "order_status", "currency"
).withColumn("order_date", F.to_timestamp("order_date", "yyyy-MM-dd HH:mm:ss"))

items = clean_strings(spark.table("bronze_order_items")).select(
    "order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_pct"
).withColumn("quantity", F.col("quantity").cast("int")
).withColumn("unit_price", F.col("unit_price").cast(MONEY)
).withColumn("discount_pct", F.col("discount_pct").cast(MONEY))

payments = clean_strings(spark.table("bronze_payments")).select(
    "payment_id", "order_id", "payment_method", "payment_status", "payment_date"
).withColumn("payment_date", F.to_timestamp("payment_date", "yyyy-MM-dd HH:mm:ss"))

for df, key in [(customers, "customer_id"), (products, "product_id"),
                (orders, "order_id"), (items, "order_item_id"),
                (payments, "payment_id")]:
    check_primary_key(df, key)

assert customers.filter(F.col("signup_date").isNull()).count() == 0
assert products.filter(F.col("unit_price").isNull() | (F.col("unit_price") <= 0) |
                       F.col("is_active").isNull()).count() == 0
assert orders.filter(F.col("order_date").isNull() |
                     ~F.col("order_status").isin("Completed", "Shipped", "Pending", "Cancelled")).count() == 0
assert items.filter(F.col("quantity").isNull() | (F.col("quantity") <= 0) |
                    F.col("unit_price").isNull() | (F.col("unit_price") <= 0) |
                    F.col("discount_pct").isNull() | (F.col("discount_pct") < 0) |
                    (F.col("discount_pct") > 100)).count() == 0
assert payments.filter(F.col("payment_date").isNull()).count() == 0

assert orders.join(customers, "customer_id", "left_anti").count() == 0
assert items.join(orders, "order_id", "left_anti").count() == 0
assert items.join(products, "product_id", "left_anti").count() == 0
assert payments.join(orders, "order_id", "left_anti").count() == 0
assert payments.groupBy("order_id").count().filter("count > 1").count() == 0

for name, df in [("silver_customers", customers), ("silver_products", products),
                 ("silver_orders", orders), ("silver_order_items", items),
                 ("silver_payments", payments)]:
    df.write.format("delta").mode("overwrite").option(
        "overwriteSchema", "true").saveAsTable(name)
    print(f"{name}: {df.count()} records")

print("Silver integrity checks passed")
