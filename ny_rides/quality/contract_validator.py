from ny_rides.contracts.yellow_taxi_contract import (
    YellowTaxiContract,
)
import pandas as pd

try:
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
except Exception:  # pragma: no cover
    SparkDataFrame = None


class ContractValidator:

    @staticmethod
    def _is_spark_df(df) -> bool:
        return SparkDataFrame is not None and isinstance(df, SparkDataFrame)

    @staticmethod
    def _validate_column_types_pandas(df: pd.DataFrame):
        errors = []

        for column, expected_type in YellowTaxiContract.COLUMN_TYPE_RULES.items():
            series = df[column]

            if expected_type == "integer" and not pd.api.types.is_integer_dtype(series):
                errors.append(f"{column} must be integer")
            elif expected_type == "numeric" and not pd.api.types.is_numeric_dtype(series):
                errors.append(f"{column} must be numeric")
            elif expected_type == "datetime" and not pd.api.types.is_datetime64_any_dtype(series):
                errors.append(f"{column} must be datetime")

        if errors:
            raise ValueError(
                "Invalid column types: " + "; ".join(errors)
            )

    @staticmethod
    def _validate_column_types_spark(df):
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
    def validate_columns(df):
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
    def validate_column_types(df):
        if ContractValidator._is_spark_df(df):
            ContractValidator._validate_column_types_spark(df)
            return

        ContractValidator._validate_column_types_pandas(df)

    @staticmethod
    def validate(df):
        ContractValidator.validate_columns(df)
        ContractValidator.validate_column_types(df)