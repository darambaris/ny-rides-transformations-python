import pytest

from ny_rides.storage.local_storage import LocalStorage


def test_should_save_file(tmp_path):
    storage = LocalStorage(base_path=str(tmp_path))

    content = b"test content"

    saved_path = storage.save(
        filename="file.parquet",
        content=content,
    )

    assert saved_path.exists()
    assert saved_path.read_bytes() == content


def test_should_create_directory_if_not_exists(
    tmp_path,
):
    storage = LocalStorage(base_path=str(tmp_path / "nested/directory"))

    content = b"test content"

    saved_path = storage.save(
        filename="file.parquet",
        content=content,
    )

    assert saved_path.exists()
    assert saved_path.parent.is_dir()
    assert saved_path.read_bytes() == content


def test_should_raise_value_error_for_empty_content(
    tmp_path,
):
    storage = LocalStorage(base_path=str(tmp_path))

    with pytest.raises(
        ValueError,
        match="Cannot save empty content",
    ):
        storage.save(
            filename="file.parquet",
            content=b"",
        )


def test_should_raise_os_error_when_write_fails(
    mocker,
    tmp_path,
):
    storage = LocalStorage(base_path=str(tmp_path))

    mocker.patch(
        "pathlib.Path.write_bytes",
        side_effect=OSError("Disk full"),
    )

    with pytest.raises(
        OSError,
        match="Disk full",
    ):
        storage.save(
            filename="file.parquet",
            content=b"content",
        )
