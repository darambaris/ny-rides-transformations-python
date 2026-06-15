
from ny_rides.ingestion.tlc_downloader import TLCDownloader, DataFile

from datetime import date
import requests

import pytest


def test_should_raise_value_error_in_generate_files():
    downloader = TLCDownloader()

    with pytest.raises(
        ValueError, match="End date must be greater than or equal to start date."
    ):
        downloader.generate_files(
            start_date=date(2024, 1, 1),
            end_date=date(2023, 12, 31),
        )


def test_should_generate_files():
    downloader = TLCDownloader()

    files = downloader.generate_files(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31),
    )

    expected = [
        DataFile(
            name="yellow_tripdata_2024-01.parquet",
            url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet",
        ),
        DataFile(
            name="yellow_tripdata_2024-02.parquet",
            url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet",
        ),
        DataFile(
            name="yellow_tripdata_2024-03.parquet",
            url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet",
        ),
    ]

    assert files == expected
    assert len(files) == 3


def test_should_generate_files_across_years():
    downloader = TLCDownloader()

    files = downloader.generate_files(
        start_date=date(2023, 11, 1),
        end_date=date(2024, 2, 29),
    )

    expected = [
        DataFile(
            name="yellow_tripdata_2023-11.parquet",
            url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-11.parquet",
        ),
        DataFile(
            name="yellow_tripdata_2023-12.parquet",
            url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-12.parquet",
        ),
        DataFile(
            name="yellow_tripdata_2024-01.parquet",
            url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet",
        ),
        DataFile(
            name="yellow_tripdata_2024-02.parquet",
            url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet",
        ),
    ]

    assert len(files) == 4

    assert files == expected