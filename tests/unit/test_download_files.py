from ny_rides.ingestion.tlc_downloader import TLCDownloader
from datetime import date

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

    assert len(files) == 3
    assert files[0].name == "yellow_tripdata_2024-01.parquet"
    assert (
        files[0].url
        == "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
    )
    assert files[1].name == "yellow_tripdata_2024-02.parquet"
    assert (
        files[1].url
        == "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet"
    )
    assert files[2].name == "yellow_tripdata_2024-03.parquet"
    assert (
        files[2].url
        == "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet"
    )


def test_should_generate_files_across_years():
    downloader = TLCDownloader()

    files = downloader.generate_files(
        start_date=date(2023, 11, 1),
        end_date=date(2024, 2, 29),
    )

    assert len(files) == 4

    assert files[0].name == "yellow_tripdata_2023-11.parquet"
    assert files[1].name == "yellow_tripdata_2023-12.parquet"
    assert files[2].name == "yellow_tripdata_2024-01.parquet"
    assert files[3].name == "yellow_tripdata_2024-02.parquet"
