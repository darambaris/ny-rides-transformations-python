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
    spark.read.parquet("data/silver")
    .filter(F.month(F.col("tpep_pickup_datetime")) == 5)
    .groupBy(F.hour(F.col("tpep_pickup_datetime")).alias("pickup_hour"))
    .agg(F.round(F.avg("passenger_count"), 2).alias("avg_passenger_count"))
    .orderBy("pickup_hour")
)
print("Q2")
q2.show(24)

spark.stop()
PY
