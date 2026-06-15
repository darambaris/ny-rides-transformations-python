from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import date

from ny_rides.ingestion.tlc_downloader import TLCDownloader
from ny_rides.shared.logging import configure_logging

import logging

logger = logging.getLogger(__name__)


@dataclass
class DownloadResult:
    file_name: str
    success: bool
    error_message: str | None = None


def execute(start_date: date, end_date: date) -> list[DownloadResult]:

    downloader = TLCDownloader()

    results = []

    files = downloader.generate_files(
        start_date=start_date,
        end_date=end_date,
    )

    for file in files:
        try:
            downloader.download_file(file)
            results.append(DownloadResult(file_name=file.name, success=True))
        except Exception as e:
            logger.exception("Failed to download file %s", file.name)
            results.append(
                DownloadResult(file_name=file.name, success=False, error_message=str(e))
            )

    return results


def log_summary(results: list[DownloadResult]) -> None:
    total = len(results)

    successful_downloads = sum(1 for result in results if result.success)

    failed_downloads = total - successful_downloads

    message = (
        "Download Summary | "
        f"Total={total} "
        f"Successful={successful_downloads} "
        f"Failed={failed_downloads}"
    )

    if failed_downloads == 0:
        logger.info(message)
    else:
        logger.warning(message)



def main():

    configure_logging()

    parser = ArgumentParser()

    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)

    args = parser.parse_args()

    results = execute(
        start_date=date.fromisoformat(args.start_date),
        end_date=date.fromisoformat(args.end_date),
    )

    log_summary(results)


if __name__ == "__main__":
    main()
