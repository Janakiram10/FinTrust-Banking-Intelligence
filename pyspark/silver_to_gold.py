"""Create a daily channel KPI Delta table."""
from pyspark.sql import functions as F

SILVER = "abfss://silver@<storage-account>.dfs.core.windows.net/fintrust"
GOLD = "abfss://gold@<storage-account>.dfs.core.windows.net/fintrust"

tx = spark.read.format("delta").load(f"{SILVER}/transactions")
gold = (tx.filter(F.col("status") == "Completed")
  .groupBy("transaction_date", "channel")
  .agg(F.count("*").alias("transaction_count"), F.sum("amount").alias("transaction_value"), F.avg("is_high_risk").alias("high_risk_rate")))
gold.write.format("delta").mode("overwrite").save(f"{GOLD}/daily_channel_kpis")

