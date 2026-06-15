from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import date
import re

from ny_rides.ingestion.tlc_downloader import TLCDownloader
from ny_rides.shared.logging import configure_logging

from ny_rides.metadata.manifest_ingestion_writer import write_manifest
from ny_rides.storage.local_storage import LocalStorage

import logging

logger = logging.getLogger(__name__)


def build_partitioned_path(file_name: str) -> str:
    match = re.search(r"_(\d{4})-(\d{2})\.parquet$", file_name)
    if not match:
        return file_name

    year, month = match.groups()
    return f"year={year}/month={month}/{file_name}"


@dataclass
class DownloadResult:
    file_name: str
    success: bool
    error_message: str | None = None


def execute(
    start_date: date,
    end_date: date,
    output_dir: str,
) -> list[DownloadResult]:

    downloader = TLCDownloader()

    results = []

    files = downloader.generate_files(
        start_date=start_date,
        end_date=end_date,
    )

    storage = LocalStorage(base_path=output_dir)

    for file in files:
        try:
            content = downloader.download_file(file)
            output_file_path = build_partitioned_path(file.name)
            storage.save(filename=output_file_path, content=content)
            results.append(DownloadResult(file_name=file.name, success=True))
        except Exception as e:
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
    parser.add_argument("--output-dir", required=True)

    args = parser.parse_args()

    results = execute(
        start_date=date.fromisoformat(args.start_date),
        end_date=date.fromisoformat(args.end_date),
        output_dir=args.output_dir,
    )

    log_summary(results)

    manifest_path = write_manifest(results)
    logger.info("Manifest saved to %s", manifest_path)


if __name__ == "__main__":
    main()
