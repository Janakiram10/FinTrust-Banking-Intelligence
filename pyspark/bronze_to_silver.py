"""Databricks-compatible Bronze to Silver Delta transformation."""
from pyspark.sql import functions as F

RAW = "abfss://bronze@<storage-account>.dfs.core.windows.net/fintrust"
SILVER = "abfss://silver@<storage-account>.dfs.core.windows.net/fintrust"

def clean_transactions(spark):
    df = spark.read.option("header", True).option("inferSchema", True).csv(f"{RAW}/transactions.csv")
    clean = (df.dropDuplicates(["transaction_id"])
        .filter(F.col("amount") > 0)
        .withColumn("transaction_ts", F.to_timestamp("transaction_ts"))
        .withColumn("transaction_date", F.to_date("transaction_ts"))
        .withColumn("risk_band", F.when(F.col("risk_score") >= .72,"High").when(F.col("risk_score") >= .4,"Medium").otherwise("Low")))
    clean.write.format("delta").mode("overwrite").option("overwriteSchema", True).save(f"{SILVER}/transactions")

if __name__ == "__main__":
    clean_transactions(spark)  # Databricks injects the Spark session

