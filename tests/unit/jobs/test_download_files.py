from datetime import date

from ny_rides.jobs.download_files import execute
from ny_rides.ingestion.tlc_downloader import DataFile

from ny_rides.jobs.download_files import (
    DownloadResult,
    log_summary,
)


def test_should_download_all_files_successfully(mocker):
    mock_downloader = mocker.Mock()

    files = [
        DataFile(
            name="yellow_tripdata_2024-01.parquet",
            url="url1",
        ),
        DataFile(
            name="yellow_tripdata_2024-02.parquet",
            url="url2",
        ),
    ]

    mock_downloader.generate_files.return_value = files

    mocker.patch(
        "ny_rides.jobs.download_files.TLCDownloader",
        return_value=mock_downloader,
    )

    results = execute(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 2, 29),
    )

    assert len(results) == 2

    assert results[0].success is True
    assert results[1].success is True

    assert mock_downloader.download_file.call_count == 2


def test_should_continue_when_download_fails(mocker):
    mock_downloader = mocker.Mock()

    files = [
        DataFile(
            name="file1.parquet",
            url="url1",
        ),
        DataFile(
            name="file2.parquet",
            url="url2",
        ),
    ]

    mock_downloader.generate_files.return_value = files

    mock_downloader.download_file.side_effect = [
        None,
        Exception("Download failed"),
    ]

    mocker.patch(
        "ny_rides.jobs.download_files.TLCDownloader",
        return_value=mock_downloader,
    )

    results = execute(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 2, 29),
    )

    assert len(results) == 2

    assert results[0].success is True

    assert results[1].success is False
    assert results[1].error_message == "Download failed"


def test_should_log_warning_when_downloads_fail(
    mocker,
):
    mock_logger = mocker.patch("ny_rides.jobs.download_files.logger")

    results = [
        DownloadResult(
            file_name="file.parquet",
            success=False,
            error_message="error",
        )
    ]

    log_summary(results)

    mock_logger.warning.assert_called()


def test_should_log_info_when_all_downloads_succeed(
    mocker,
):
    mock_logger = mocker.patch("ny_rides.jobs.download_files.logger")

    results = [
        DownloadResult(
            file_name="file.parquet",
            success=True,
        )
    ]

    log_summary(results)

    mock_logger.info.assert_called_once()
    mock_logger.warning.assert_not_called()
