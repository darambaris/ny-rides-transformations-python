from argparse import ArgumentParser
import logging

from ny_rides.shared.spark import get_spark_session
from ny_rides.shared.logging import configure_logging
from ny_rides.data_transformations.gold_transformer import GoldTransformer


LOGGER = logging.getLogger(__name__)


class BuildGoldJob:

    def __init__(
        self,
        spark,
        transformer,
    ):
        self.spark = spark
        self.transformer = transformer

    def execute(
        self,
        silver_path: str,
        gold_path: str,
    ):
        LOGGER.info(
            "Starting gold build. silver_path=%s gold_path=%s",
            silver_path,
            gold_path,
        )

        silver_df = self.spark.read.parquet(silver_path)
        silver_rows = silver_df.count()
        LOGGER.info("Silver dataset loaded. rows=%s", silver_rows)

        monthly_average_df = self.transformer.build_monthly_average_total_amount(
            silver_df
        )
        monthly_output_path = f"{gold_path}/monthly_average_total_amount"
        monthly_average_df.write.mode("overwrite").parquet(monthly_output_path)
        monthly_rows = monthly_average_df.count()
        LOGGER.info(
            "Monthly average total_amount dataset written. path=%s rows=%s",
            monthly_output_path,
            monthly_rows,
        )

        may_hourly_df = self.transformer.build_hourly_average_passenger_count(
            silver_df
        )
        hourly_output_path = f"{gold_path}/hourly_average_passenger_count"
        may_hourly_df.write.mode("overwrite").parquet(hourly_output_path)
        hourly_rows = may_hourly_df.count()
        LOGGER.info(
            "Hourly average passenger_count dataset written. path=%s rows=%s",
            hourly_output_path,
            hourly_rows,
        )

        LOGGER.info("Gold build completed successfully")


def main():
    configure_logging()

    parser = ArgumentParser()
    parser.add_argument("--silver-path", required=True)
    parser.add_argument("--gold-path", required=True)

    args = parser.parse_args()

    spark = get_spark_session(app_name="Build Gold Job")
    transformer = GoldTransformer()

    job = BuildGoldJob(spark=spark, transformer=transformer)
    job.execute(silver_path=args.silver_path, gold_path=args.gold_path)


if __name__ == "__main__":
    main()