from ny_rides.contracts.yellow_taxi_contract import (
    YellowTaxiContract,
)
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql.types import (
    DateType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    ShortType,
    TimestampNTZType,
    TimestampType,
)


class ContractValidator:

    @staticmethod
    def _validate_column_types_spark(df: SparkDataFrame):
        errors = []
        schema_by_col = {
            field.name: field.dataType
            for field in df.schema.fields
        }

        for column, expected_type in YellowTaxiContract.COLUMN_TYPE_RULES.items():
            data_type = schema_by_col.get(column)

            if expected_type == "integer" and not isinstance(
                data_type, (IntegerType, LongType, ShortType)
            ):
                errors.append(f"{column} must be integer")
            elif expected_type == "numeric" and not isinstance(
                data_type, (IntegerType, LongType, ShortType, FloatType, DoubleType, DecimalType)
            ):
                errors.append(f"{column} must be numeric")
            elif expected_type == "datetime" and not isinstance(
                data_type, (TimestampType, TimestampNTZType, DateType)
            ):
                errors.append(f"{column} must be datetime")

        if errors:
            raise ValueError(
                "Invalid column types: " + "; ".join(errors)
            )

    @staticmethod
    def validate_columns(df: SparkDataFrame):
        missing_columns = (
            set(
                YellowTaxiContract.REQUIRED_COLUMNS
            )
            - set(df.columns)
        )

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}"
            )

    @staticmethod
    def validate_column_types(df: SparkDataFrame):
        ContractValidator._validate_column_types_spark(df)

    @staticmethod
    def validate(df: SparkDataFrame):
        ContractValidator.validate_columns(df)
        ContractValidator.validate_column_types(df)