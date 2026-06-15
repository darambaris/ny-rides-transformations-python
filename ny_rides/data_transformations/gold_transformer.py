from pyspark.sql import functions as F


class GoldTransformer:

    def build_monthly_average_total_amount(
        self,
        dataframe,
    ):
        """
        Aggregate dataset with monthly average total_amount across all yellow taxis.
        
        Returns a DataFrame with columns:
        - pickup_year
        - pickup_month
        - avg_total_amount
        """
        return (
            dataframe.groupBy("pickup_year", "pickup_month")
            .agg(F.round(F.avg("total_amount"), 2).alias("avg_total_amount"))
            .orderBy("pickup_year", "pickup_month")
        )

    def build_hourly_average_passenger_count(
        self,
        dataframe,
    ):
        """
        Aggregate dataset with hourly average passenger_count across all yellow taxis.
        
        Returns a DataFrame with columns:
        - pickup_hour
        - avg_passenger_count
        """
        return (
            dataframe.withColumn("pickup_hour", F.hour("tpep_pickup_datetime"))
            .groupBy("pickup_hour")
            .agg(F.round(F.avg("passenger_count"), 2).alias("avg_passenger_count"))
            .orderBy("pickup_hour")
        )