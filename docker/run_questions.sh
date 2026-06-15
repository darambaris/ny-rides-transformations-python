#!/usr/bin/env sh
set -e

python - <<'PY'
from ny_rides.shared.spark import get_spark_session
from pyspark.sql import functions as F

spark = get_spark_session("Questions")

q1 = (
    spark.read.parquet("data/gold/monthly_average_total_amount")
    .filter((F.col("pickup_year") == 2025) & (F.col("pickup_month") <= 5))
    .orderBy("pickup_year", "pickup_month")
)
print("Q1")
q1.show()

q2 = (
    spark.read.parquet("data/gold/hourly_average_passenger_count")
    .filter((F.col("pickup_year") == 2025) & (F.col("pickup_month") == 5))
    .withColumn("avg_passenger_count", F.round(F.col("avg_passenger_count"), 2))
    .orderBy("pickup_hour")
)
print("Q2")
q2.show(24)

spark.stop()
PY
