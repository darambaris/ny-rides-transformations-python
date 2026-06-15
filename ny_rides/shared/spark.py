import os

from pyspark.sql import SparkSession


def get_spark_session(
    app_name: str,
) -> SparkSession:
    os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")

    spark = (
        SparkSession.builder.appName(app_name)
        .config("spark.driver.memory", "4g")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.files.maxPartitionBytes", str(256 * 1024 * 1024))
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")
    return spark
