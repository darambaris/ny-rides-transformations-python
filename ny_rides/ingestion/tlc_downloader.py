from dataclasses import dataclass
from datetime import date
import logging

import requests


@dataclass
class DataFile:
    name: str
    url: str


class TLCDownloader:
    BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_files(self, start_date: date, end_date: date) -> list[DataFile]:

        # valid range
        if end_date < start_date:
            raise ValueError("End date must be greater than or equal to start date.")

        start_month = date(start_date.year, start_date.month, 1)
        end_month = date(end_date.year, end_date.month, 1)

        files: list[DataFile] = []

        self.logger.info(f"Generating file list from {start_month} to {end_month}")

        while start_month <= end_month:
            file_name = (
                f"yellow_tripdata_{start_month.year}-{start_month.month:02d}.parquet"
            )
            url = f"{self.BASE_URL}/{file_name}"
            files.append(DataFile(name=file_name, url=url))

            # move to the next month
            if start_month.month == 12:
                start_month = date(start_month.year + 1, 1, 1)
            else:
                start_month = date(start_month.year, start_month.month + 1, 1)

        return files

    def download_file(self, data_file: DataFile) -> bytes:
        self.logger.info(f"Downloading {data_file.url}")

        try:
            response = requests.get(data_file.url, timeout=30)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            self.logger.exception(f"Failed to download {data_file.url}: {e}")
            raise RuntimeError(f"Download failed for {data_file.name}") from e
