import json
from datetime import datetime
from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from ny_rides.contracts.yellow_taxi_contract import YellowTaxiContract


class QualityValidator:
    @staticmethod
    def _failure_percentage(failed_rows, total_rows: int):
        if failed_rows is None:
            return None
        if total_rows == 0:
            return 0.0
        return round((failed_rows / total_rows) * 100, 4)

    @staticmethod
    def validate(df: DataFrame) -> dict:
        total_rows = df.count()
        checks = []

        if "total_amount" in df.columns:
            negative_total_amount = df.filter(F.col("total_amount") < 0).count()
            checks.append(
                {
                    "name": "total_amount >= 0",
                    "passed": negative_total_amount == 0,
                    "failed_rows": negative_total_amount,
                    "failure_percentage": QualityValidator._failure_percentage(
                        negative_total_amount,
                        total_rows,
                    ),
                }
            )
        else:
            checks.append(
                {
                    "name": "total_amount >= 0",
                    "passed": False,
                    "failed_rows": None,
                    "failure_percentage": None,
                    "details": "Column total_amount not found",
                }
            )

        if {
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
        }.issubset(set(df.columns)):
            invalid_pickup_dropoff = df.filter(
                F.col("tpep_pickup_datetime") > F.col("tpep_dropoff_datetime")
            ).count()
            checks.append(
                {
                    "name": "pickup <= dropoff",
                    "passed": invalid_pickup_dropoff == 0,
                    "failed_rows": invalid_pickup_dropoff,
                    "failure_percentage": QualityValidator._failure_percentage(
                        invalid_pickup_dropoff,
                        total_rows,
                    ),
                }
            )
        else:
            checks.append(
                {
                    "name": "pickup <= dropoff",
                    "passed": False,
                    "failed_rows": None,
                    "failure_percentage": None,
                    "details": "Datetime columns not found",
                }
            )

        required_columns = YellowTaxiContract.REQUIRED_COLUMNS
        missing_required_columns = sorted(set(required_columns) - set(df.columns))
        if missing_required_columns:
            checks.append(
                {
                    "name": "no nulls in required columns",
                    "passed": False,
                    "failed_rows": None,
                    "failure_percentage": None,
                    "details": f"Missing required columns: {missing_required_columns}",
                }
            )
        else:
            null_agg = (
                df.agg(
                    *[
                        F.sum(F.when(F.col(column).isNull(), 1).otherwise(0)).alias(
                            column
                        )
                        for column in required_columns
                    ]
                )
                .collect()[0]
                .asDict()
            )
            total_required_nulls = int(sum(null_agg.values()))
            checks.append(
                {
                    "name": "no nulls in required columns",
                    "passed": total_required_nulls == 0,
                    "failed_rows": total_required_nulls,
                    "failure_percentage": QualityValidator._failure_percentage(
                        total_required_nulls,
                        total_rows,
                    ),
                }
            )

        duplicated_rows = total_rows - df.dropDuplicates().count()
        checks.append(
            {
                "name": "duplicados",
                "passed": duplicated_rows == 0,
                "failed_rows": int(duplicated_rows),
                "failure_percentage": QualityValidator._failure_percentage(
                    int(duplicated_rows),
                    total_rows,
                ),
            }
        )

        all_checks_passed = all(check["passed"] for check in checks)

        return {
            "execution_timestamp": datetime.now().isoformat(),
            "total_rows": int(total_rows),
            "all_checks_passed": all_checks_passed,
            "checks": checks,
        }

    @staticmethod
    def write_report(report: dict, output_dir: str = "artifacts/quality") -> Path:
        timestamp = datetime.now()
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        report_path = (
            output_path / f"quality_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        )
        report_path.write_text(json.dumps(report, indent=2))

        return report_path
