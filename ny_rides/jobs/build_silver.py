from argparse import ArgumentParser
import logging

from ny_rides.shared.spark import get_spark_session
from ny_rides.shared.logging import configure_logging
from ny_rides.quality.contract_validator import ContractValidator
from ny_rides.quality.quality_validator import QualityValidator
from ny_rides.metadata.manifest_quality_writer import write_manifest
from ny_rides.data_transformations.silver_transformer import SilverTransformer


LOGGER = logging.getLogger(__name__)


class BuildSilverJob:
    def __init__(
        self,
        spark,
        validator,
        transformer,
        quality_validator,
        quality_report_dir: str = "artifacts/quality",
    ):
        self.spark = spark
        self.validator = validator
        self.transformer = transformer
        self.quality_validator = quality_validator
        self.quality_report_dir = quality_report_dir

    def execute(self, raw_path: str, silver_path: str):
        LOGGER.info(
            "Starting silver build. raw_path=%s silver_path=%s",
            raw_path,
            silver_path,
        )

        raw_df = self.spark.read.parquet(raw_path)
        raw_columns_data = getattr(raw_df, "columns", [])
        raw_columns = (
            len(raw_columns_data) if isinstance(raw_columns_data, (list, tuple)) else 0
        )
        LOGGER.info("Raw dataset loaded with %s columns", raw_columns)

        self.validator.validate(raw_df)
        LOGGER.info("Raw dataset contract validation passed")

        silver_df = self.transformer.transform(raw_df)
        LOGGER.info("Silver transformation completed")

        LOGGER.info(
            "Writing silver dataset to %s partitioned by pickup_year,pickup_month",
            silver_path,
        )
        silver_df.write.mode("overwrite").partitionBy(
            "pickup_year",
            "pickup_month",
        ).parquet(silver_path)

        # Confirm write by reading back the destination path.
        written_df = self.spark.read.parquet(silver_path)
        written_rows = written_df.count()
        LOGGER.info(
            "Silver write completed successfully. path=%s rows=%s",
            silver_path,
            written_rows,
        )

        try:
            quality_report = self.quality_validator.validate(written_df)
            report_path = write_manifest(
                quality_report,
                output_dir=self.quality_report_dir,
            )
            LOGGER.info(
                "Quality report generated. path=%s all_checks_passed=%s",
                report_path,
                quality_report.get("all_checks_passed"),
            )
        except Exception:
            LOGGER.exception(
                "Quality validation/report failed, but silver parquet generation will not be blocked"
            )


def main():
    configure_logging()

    parser = ArgumentParser()
    parser.add_argument("--raw-path", required=True)
    parser.add_argument("--silver-path", required=True)
    parser.add_argument("--quality-report-dir", default="artifacts/quality/silver")

    args = parser.parse_args()

    spark = get_spark_session(app_name="Build Silver Job")
    validator = ContractValidator()
    quality_validator = QualityValidator()
    transformer = SilverTransformer()

    job = BuildSilverJob(
        spark=spark,
        validator=validator,
        transformer=transformer,
        quality_validator=quality_validator,
        quality_report_dir=args.quality_report_dir,
    )

    job.execute(
        raw_path=args.raw_path,
        silver_path=args.silver_path,
    )


if __name__ == "__main__":
    main()
