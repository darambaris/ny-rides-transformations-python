from dataclasses import dataclass


@dataclass(frozen=True)
class YellowTaxiContract:
    required_columns = [
        "VendorID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "fare_amount",
    ]