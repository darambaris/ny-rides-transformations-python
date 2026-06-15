from ny_rides.quality.contract_validator import ContractValidator
import pytest
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)


class FakeSparkDataFrame:
    def __init__(self, columns, schema):
        self.columns = columns
        self.schema = schema


def _valid_dataframe():
    columns = [
        "VendorID",
        "passenger_count",
        "total_amount",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]
    schema = StructType(
        [
            StructField("VendorID", IntegerType(), True),
            StructField("passenger_count", IntegerType(), True),
            StructField("total_amount", DoubleType(), True),
            StructField("tpep_pickup_datetime", TimestampType(), True),
            StructField("tpep_dropoff_datetime", TimestampType(), True),
        ]
    )
    return FakeSparkDataFrame(columns=columns, schema=schema)


def test_should_accept_valid_schema():
    df = _valid_dataframe()

    ContractValidator.validate_columns(df)


def test_should_fail_when_required_column_is_missing():
    valid_df = _valid_dataframe()
    df = FakeSparkDataFrame(
        columns=[c for c in valid_df.columns if c != "total_amount"],
        schema=valid_df.schema,
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        ContractValidator.validate_columns(df)


def test_should_accept_valid_column_types():
    df = _valid_dataframe()

    ContractValidator.validate_column_types(df)


def test_should_fail_when_column_types_are_invalid():
    df = FakeSparkDataFrame(
        columns=[
            "VendorID",
            "passenger_count",
            "total_amount",
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
        ],
        schema=StructType(
            [
                StructField("VendorID", IntegerType(), True),
                StructField("passenger_count", DoubleType(), True),
                StructField("total_amount", DoubleType(), True),
                StructField("tpep_pickup_datetime", StringType(), True),
                StructField("tpep_dropoff_datetime", TimestampType(), True),
            ]
        ),
    )

    with pytest.raises(
        ValueError,
        match="Schema validation failed",
    ):
        ContractValidator.validate_column_types(df)


def test_should_validate_columns_and_types_together():
    df = _valid_dataframe()

    ContractValidator.validate(df)
