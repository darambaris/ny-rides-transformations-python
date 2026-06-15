from ny_rides.jobs.download_files import TLCDownloader
from datetime import date

import pytest

def test_should_raise_value_error_in_generate_files():
    downloader = TLCDownloader(config={})

    with pytest.raises(
        ValueError,
        match="End date must be greater than or equal to start date."
    ):
        downloader.generate_files(
            start_date=date(2024, 1, 1),
            end_date=date(2023, 12, 31),
        )

