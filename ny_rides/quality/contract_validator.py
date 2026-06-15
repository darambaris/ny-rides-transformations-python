from ny_rides.contracts.yellow_taxi_contract import (
    YellowTaxiContract,
)


class ContractValidator:

    @staticmethod
    def validate_columns(df):
        missing_columns = (
            set(
                YellowTaxiContract.required_columns
            )
            - set(df.columns)
        )

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}"
            )