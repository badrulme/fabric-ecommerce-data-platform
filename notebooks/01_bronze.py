# Fabric Notebook 01 — Bronze. Attach lh_ecom_bronze as DEFAULT Lakehouse.
# Run only after Data Factory copied 5 CSV files to Files/raw/.
from pyspark.sql import functions as F

for name in ["customers", "products", "orders", "order_items", "payments"]:
    source = f"Files/raw/{name}.csv"
    df = (spark.read.option("header", True).option("inferSchema", False)
          .option("mode", "FAILFAST").csv(source)
          .withColumn("_ingestion_ts", F.current_timestamp())
          .withColumn("_source_file", F.lit(source)))
    df.write.format("delta").mode("overwrite").option(
        "overwriteSchema", "true").saveAsTable(f"bronze_{name}")
    print(f"bronze_{name}: {df.count()} records")
