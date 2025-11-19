# Databricks notebook source
# MAGIC %md
# MAGIC # Example PySpark Job
# MAGIC 
# MAGIC This is a simple example PySpark job that demonstrates basic functionality.

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count

# Create Spark session
spark = SparkSession.builder.appName("ExamplePySparkJob").getOrCreate()

print("=" * 50)
print("Example PySpark Job Started")
print("=" * 50)

# COMMAND ----------

# Example: Create a simple DataFrame
data = [
    ("category1", 100.0),
    ("category1", 200.0),
    ("category2", 150.0),
    ("category2", 250.0),
    ("category3", 300.0),
]

df = spark.createDataFrame(data, ["category", "amount"])

print(f"\nTotal rows: {df.count()}")
print("\nData sample:")
df.show()

# COMMAND ----------

# Example: Aggregate data
result = df \
    .groupBy("category") \
    .agg(
        sum("amount").alias("total_amount"),
        avg("amount").alias("avg_amount"),
        count("*").alias("count")
    )

print("\nAggregated results:")
result.show()

# COMMAND ----------

print("\n" + "=" * 50)
print("Example PySpark Job Completed Successfully!")
print("=" * 50)

spark.stop()

