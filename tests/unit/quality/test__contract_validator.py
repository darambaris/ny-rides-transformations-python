from ny_rides.quality.contract_validator import ContractValidator
import pandas as pd
import pytest


def _valid_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "VendorID": [1, 2],
            "tpep_pickup_datetime": pd.to_datetime(
                [
                    "2025-01-01 10:00:00",
                    "2025-01-01 11:00:00",
                ]
            ),
            "tpep_dropoff_datetime": pd.to_datetime(
                [
                    "2025-01-01 10:20:00",
                    "2025-01-01 11:15:00",
                ]
            ),
            "passenger_count": [1, 2],
            "trip_distance": [2.4, 5.1],
            "fare_amount": [12.5, 19.8],
        }
    )


def test_should_accept_valid_schema():
    df = _valid_dataframe()

    ContractValidator.validate_columns(df)


def test_should_fail_when_required_column_is_missing():
    df = _valid_dataframe().drop(columns=["fare_amount"])

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        ContractValidator.validate_columns(df)


def test_should_accept_valid_column_types():
    df = _valid_dataframe()

    ContractValidator.validate_column_types(df)


def test_should_fail_when_column_types_are_invalid():
    df = _valid_dataframe().copy()
    df["passenger_count"] = df["passenger_count"].astype(float)
    df["tpep_pickup_datetime"] = df["tpep_pickup_datetime"].astype(str)

    with pytest.raises(
        ValueError,
        match="Invalid column types",
    ):
        ContractValidator.validate_column_types(df)


def test_should_validate_columns_and_types_together():
    df = _valid_dataframe()

    ContractValidator.validate(df)