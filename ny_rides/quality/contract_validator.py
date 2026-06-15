from ny_rides.contracts.yellow_taxi_contract import (
    YellowTaxiContract,
)
import pandas as pd


class ContractValidator:

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
    def validate_column_types(df: pd.DataFrame):
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
    def validate(df: pd.DataFrame):
        ContractValidator.validate_columns(df)
        ContractValidator.validate_column_types(df)