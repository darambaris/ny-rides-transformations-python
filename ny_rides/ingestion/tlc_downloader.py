from dataclasses import dataclass
from datetime import date
import logging


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
