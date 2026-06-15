from ny_rides.quality.contract_validator import ContractValidator
from pyspark.sql.functions import lit

import pytest
import subprocess


def _has_java_runtime() -> bool:
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


JAVA_AVAILABLE = _has_java_runtime()


@pytest.mark.skipif(
    not JAVA_AVAILABLE,
    reason="Java runtime is not available for PySpark tests",
)
def test_should_accept_valid_schema(spark_session):
    df = spark_session.createDataFrame(
        [(1,)],
        ["VendorID"],
    )

    df = (
        df
        .withColumn(
            "tpep_pickup_datetime",
            lit(None),
        )
        .withColumn(
            "tpep_dropoff_datetime",
            lit(None),
        )
        .withColumn(
            "passenger_count",
            lit(1),
        )
        .withColumn(
            "trip_distance",
            lit(1.0),
        )
        .withColumn(
            "fare_amount",
            lit(10.0),
        )
    )

    ContractValidator.validate_columns(df)


@pytest.mark.skipif(
    not JAVA_AVAILABLE,
    reason="Java runtime is not available for PySpark tests",
)
def test_should_fail_when_required_column_is_missing(
    spark_session,
):
    df = spark_session.createDataFrame(
        [(1,)],
        ["VendorID"],
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        ContractValidator.validate_columns(df)