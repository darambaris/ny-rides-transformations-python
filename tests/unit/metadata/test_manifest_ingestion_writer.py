import json
from datetime import datetime

import pytest

from ny_rides.jobs.download_files import DownloadResult
from ny_rides.metadata.manifest_ingestion_writer import write_manifest


def test_should_write_manifest_with_all_successful_downloads(
    mocker,
    tmp_path,
):
    mock_now = datetime(2025, 3, 15, 10, 30, 45)
    mocker.patch(
        "ny_rides.metadata.manifest_ingestion_writer.datetime",
    ).now.return_value = mock_now

    results = [
        DownloadResult(file_name="file1.parquet", success=True),
        DownloadResult(file_name="file2.parquet", success=True),
    ]

    manifest_path = write_manifest(results, output_dir=str(tmp_path))

    assert manifest_path.exists()

    manifest_content = json.loads(manifest_path.read_text())

    assert manifest_content["execution_timestamp"] == mock_now.isoformat()
    assert manifest_content["requested_files"] == 2
    assert manifest_content["successful_files"] == 2
    assert manifest_content["failed_files"] == 0
    assert len(manifest_content["files"]) == 2
    assert manifest_content["files"][0]["file_name"] == "file1.parquet"
    assert manifest_content["files"][0]["success"] is True
    assert manifest_content["files"][0]["error"] is None


def test_should_write_manifest_with_failed_downloads(
    mocker,
    tmp_path,
):
    mock_now = datetime(2025, 3, 15, 10, 30, 45)
    mocker.patch(
        "ny_rides.metadata.manifest_ingestion_writer.datetime",
    ).now.return_value = mock_now

    results = [
        DownloadResult(file_name="file1.parquet", success=True),
        DownloadResult(
            file_name="file2.parquet",
            success=False,
            error_message="Network error",
        ),
    ]

    manifest_path = write_manifest(results, output_dir=str(tmp_path))

    assert manifest_path.exists()

    manifest_content = json.loads(manifest_path.read_text())

    assert manifest_content["requested_files"] == 2
    assert manifest_content["successful_files"] == 1
    assert manifest_content["failed_files"] == 1
    assert manifest_content["files"][1]["success"] is False
    assert manifest_content["files"][1]["error"] == "Network error"


def test_should_create_output_directory_if_not_exists(
    mocker,
    tmp_path,
):
    mock_now = datetime(2025, 3, 15, 10, 30, 45)
    mocker.patch(
        "ny_rides.metadata.manifest_ingestion_writer.datetime",
    ).now.return_value = mock_now

    results = [DownloadResult(file_name="file.parquet", success=True)]

    nested_output_dir = str(tmp_path / "nested" / "artifacts" / "ingestion")

    manifest_path = write_manifest(results, output_dir=nested_output_dir)

    assert manifest_path.exists()
    assert manifest_path.parent.is_dir()


def test_should_generate_manifest_with_timestamp_in_filename(
    mocker,
    tmp_path,
):
    mock_now = datetime(2025, 3, 15, 10, 30, 45)
    mocker.patch(
        "ny_rides.metadata.manifest_ingestion_writer.datetime",
    ).now.return_value = mock_now

    results = []

    manifest_path = write_manifest(results, output_dir=str(tmp_path))

    assert manifest_path.name == "manifest_20250315_103045.json"


def test_should_write_manifest_with_empty_results(
    mocker,
    tmp_path,
):
    mock_now = datetime(2025, 3, 15, 10, 30, 45)
    mocker.patch(
        "ny_rides.metadata.manifest_ingestion_writer.datetime",
    ).now.return_value = mock_now

    results = []

    manifest_path = write_manifest(results, output_dir=str(tmp_path))

    assert manifest_path.exists()

    manifest_content = json.loads(manifest_path.read_text())

    assert manifest_content["requested_files"] == 0
    assert manifest_content["successful_files"] == 0
    assert manifest_content["failed_files"] == 0
    assert manifest_content["files"] == []
