from argparse import ArgumentParser
from datetime import date

from ny_rides.ingestion.tlc_downloader import TLCDownloader


def main():
    parser = ArgumentParser()

    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)

    args = parser.parse_args()

    downloader = TLCDownloader()

    files = downloader.generate_files(
        start_date=date.fromisoformat(args.start_date),
        end_date=date.fromisoformat(args.end_date),
    )

    print(files)


if __name__ == "__main__":
    main()
