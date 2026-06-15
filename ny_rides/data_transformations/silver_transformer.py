from ny_rides.contracts.yellow_taxi_contract import YellowTaxiContract
from pyspark.sql.functions import col, month, unix_timestamp, year


class SilverTransformer:
    def transform(self, dataframe):
        silver_df = dataframe.select(*YellowTaxiContract.REQUIRED_COLUMNS)

        silver_df = silver_df.withColumn(
            "VendorID",
            col("VendorID").cast("integer"),
        )

        silver_df = silver_df.withColumn(
            "total_amount",
            col("total_amount").cast("double"),
        )

        silver_df = silver_df.select(
            "*",
            year(col("tpep_pickup_datetime")).alias("pickup_year"),
            month(col("tpep_pickup_datetime")).alias("pickup_month"),
        )

        silver_df = silver_df.withColumn(
            "trip_duration_minutes",
            (
                unix_timestamp(col("tpep_dropoff_datetime"))
                - unix_timestamp(col("tpep_pickup_datetime"))
            )
            / 60.0,
        )

        return silver_df
