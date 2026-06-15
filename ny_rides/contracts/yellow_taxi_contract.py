class YellowTaxiContract:
    REQUIRED_COLUMNS = [
        "VendorID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "fare_amount",
    ]

    COLUMN_TYPE_RULES = {
        "VendorID": "integer",
        "tpep_pickup_datetime": "datetime",
        "tpep_dropoff_datetime": "datetime",
        "passenger_count": "integer",
        "trip_distance": "numeric",
        "fare_amount": "numeric",
    }