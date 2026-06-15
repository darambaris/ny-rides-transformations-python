from datetime import date
from types import SimpleNamespace

from ny_rides.jobs.download_files import execute
from ny_rides.ingestion.tlc_downloader import DataFile

from ny_rides.jobs.download_files import (
    DownloadResult,
    log_summary,
    main,
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
    mock_downloader.download_file.return_value = b"file content"

    mocker.patch(
        "ny_rides.jobs.download_files.TLCDownloader",
        return_value=mock_downloader,
    )

    mocker.patch("ny_rides.jobs.download_files.LocalStorage")

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
        b"file content",
        Exception("Download failed"),
    ]

    mocker.patch(
        "ny_rides.jobs.download_files.TLCDownloader",
        return_value=mock_downloader,
    )

    mocker.patch("ny_rides.jobs.download_files.LocalStorage")

    results = execute(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 2, 29),
    )

    assert len(results) == 2

    assert results[0].success is True

    assert results[1].success is False
    assert results[1].error_message == "Download failed"


def test_should_return_empty_results_when_no_files_are_generated(
    mocker,
):
    mock_downloader = mocker.Mock()
    mock_downloader.generate_files.return_value = []

    mocker.patch(
        "ny_rides.jobs.download_files.TLCDownloader",
        return_value=mock_downloader,
    )

    mock_storage = mocker.Mock()
    mocker.patch(
        "ny_rides.jobs.download_files.LocalStorage",
        return_value=mock_storage,
    )

    results = execute(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
    )

    assert results == []
    mock_downloader.download_file.assert_not_called()
    mock_storage.save.assert_not_called()


def test_should_mark_download_as_failed_when_storage_save_fails(
    mocker,
):
    mock_downloader = mocker.Mock()

    files = [
        DataFile(
            name="file1.parquet",
            url="url1",
        )
    ]

    mock_downloader.generate_files.return_value = files
    mock_downloader.download_file.return_value = b"file content"

    mock_storage = mocker.Mock()
    mock_storage.save.side_effect = ValueError("Disk full")

    mocker.patch(
        "ny_rides.jobs.download_files.TLCDownloader",
        return_value=mock_downloader,
    )
    mocker.patch(
        "ny_rides.jobs.download_files.LocalStorage",
        return_value=mock_storage,
    )

    results = execute(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
    )

    assert len(results) == 1
    assert results[0].success is False
    assert results[0].error_message == "Disk full"


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


def test_should_include_totals_in_summary_logs(
    mocker,
):
    mock_logger = mocker.patch("ny_rides.jobs.download_files.logger")

    results = [
        DownloadResult(file_name="ok.parquet", success=True),
        DownloadResult(
            file_name="error.parquet",
            success=False,
            error_message="error",
        ),
    ]

    log_summary(results)

    mock_logger.warning.assert_called_once_with(
        "Download Summary | Total=2 Successful=1 Failed=1"
    )


def test_main_should_configure_logging_execute_and_log_summary(
    mocker,
):
    mock_parser = mocker.Mock()
    mock_parser.parse_args.return_value = SimpleNamespace(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    mock_argument_parser = mocker.patch(
        "ny_rides.jobs.download_files.ArgumentParser",
        return_value=mock_parser,
    )
    mock_configure_logging = mocker.patch(
        "ny_rides.jobs.download_files.configure_logging"
    )
    mock_execute = mocker.patch(
        "ny_rides.jobs.download_files.execute",
        return_value=[DownloadResult(file_name="file.parquet", success=True)],
    )
    mock_log_summary = mocker.patch(
        "ny_rides.jobs.download_files.log_summary"
    )

    main()

    mock_configure_logging.assert_called_once()
    mock_argument_parser.assert_called_once()
    assert mock_parser.add_argument.call_count == 2
    mock_execute.assert_called_once_with(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
    )
    mock_log_summary.assert_called_once_with(
        [DownloadResult(file_name="file.parquet", success=True)]
    )
