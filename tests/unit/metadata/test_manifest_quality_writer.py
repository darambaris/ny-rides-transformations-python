import json
from datetime import datetime

from ny_rides.metadata.manifest_quality_writer import write_manifest


def test_should_create_output_directory_if_not_exists(tmp_path):
    output_dir = tmp_path / "quality" / "silver"
    report = {
        "execution_timestamp": datetime.now().isoformat(),
        "total_rows": 100,
        "all_checks_passed": True,
        "checks": [],
    }

    write_manifest(report, str(output_dir))

    assert output_dir.exists()


def test_should_write_json_file(tmp_path):
    report = {
        "execution_timestamp": datetime.now().isoformat(),
        "total_rows": 100,
        "all_checks_passed": True,
        "checks": [],
    }

    path = write_manifest(report, str(tmp_path))

    assert path.exists()
    assert path.suffix == ".json"


def test_should_return_path_with_timestamp_filename(mocker, tmp_path):
    mock_now = datetime(2025, 3, 15, 10, 30, 45)
    mocker.patch(
        "ny_rides.metadata.manifest_quality_writer.datetime",
    ).now.return_value = mock_now

    report = {"execution_timestamp": mock_now.isoformat(), "total_rows": 100, "all_checks_passed": True, "checks": []}

    path = write_manifest(report, str(tmp_path))

    assert path.name == "quality_report_20250315_103045.json"


def test_should_write_valid_json_content(tmp_path):
    report = {
        "execution_timestamp": datetime.now().isoformat(),
        "total_rows": 1000,
        "all_checks_passed": False,
        "checks": [
            {
                "name": "total_amount >= 0",
                "passed": False,
                "failed_rows": 50,
                "failure_percentage": 5.0,
            }
        ],
    }

    path = write_manifest(report, str(tmp_path))

    loaded = json.loads(path.read_text())

    assert loaded["total_rows"] == 1000
    assert loaded["all_checks_passed"] is False
    assert len(loaded["checks"]) == 1
    assert loaded["checks"][0]["name"] == "total_amount >= 0"
    assert loaded["checks"][0]["failure_percentage"] == 5.0


def test_should_preserve_none_values(tmp_path):
    report = {
        "execution_timestamp": datetime.now().isoformat(),
        "total_rows": 100,
        "all_checks_passed": False,
        "checks": [
            {
                "name": "total_amount >= 0",
                "passed": False,
                "failed_rows": None,
                "failure_percentage": None,
                "details": "Column total_amount not found",
            }
        ],
    }

    path = write_manifest(report, str(tmp_path))

    loaded = json.loads(path.read_text())

    assert loaded["checks"][0]["failed_rows"] is None
    assert loaded["checks"][0]["failure_percentage"] is None
    assert loaded["checks"][0]["details"] == "Column total_amount not found"


def test_should_use_default_output_dir_when_not_specified(mocker):
    mock_path = mocker.MagicMock()
    mock_path.__truediv__ = mocker.MagicMock(return_value=mock_path)
    mock_path.write_text = mocker.MagicMock()

    mocker.patch(
        "ny_rides.metadata.manifest_quality_writer.Path",
        return_value=mock_path,
    )

    report = {"execution_timestamp": datetime.now().isoformat(), "total_rows": 0, "all_checks_passed": True, "checks": []}

    write_manifest(report)

    mock_path.mkdir.assert_called_once_with(parents=True, exist_ok=True)
