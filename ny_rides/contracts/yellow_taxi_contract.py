class YellowTaxiContract:
    REQUIRED_COLUMNS = [
        "VendorID",
        "passenger_count",
        "total_amount",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]

    COLUMN_TYPE_RULES = {
        "VendorID": "integer",
        "passenger_count": "numeric",
        "total_amount": "numeric",
        "tpep_pickup_datetime": "datetime",
        "tpep_dropoff_datetime": "datetime",
    }
