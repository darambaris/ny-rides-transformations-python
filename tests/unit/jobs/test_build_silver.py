from ny_rides.jobs.build_silver import BuildSilverJob


def test_should_build_silver_layer(mocker):
    spark = mocker.Mock()

    validator = mocker.Mock()
    transformer = mocker.Mock()
    quality_validator = mocker.Mock()
    mock_write_manifest = mocker.patch("ny_rides.jobs.build_silver.write_manifest")

    raw_df = mocker.Mock()
    written_df = mocker.Mock()
    silver_df = mocker.Mock()

    spark.read.parquet.side_effect = [raw_df, written_df]

    transformer.transform.return_value = silver_df
    quality_validator.validate.return_value = {"all_checks_passed": True}
    mock_write_manifest.return_value = "artifacts/quality/silver/quality_report.json"

    job = BuildSilverJob(
        spark=spark,
        validator=validator,
        transformer=transformer,
        quality_validator=quality_validator,
    )

    job.execute(
        raw_path="data/raw",
        silver_path="data/silver",
    )

    validator.validate.assert_called_once_with(raw_df)

    transformer.transform.assert_called_once_with(raw_df)

    silver_df.write.mode.assert_called_once_with("overwrite")

    silver_df.write.mode.return_value.partitionBy.assert_called_once_with(
        "pickup_year",
        "pickup_month",
    )

    silver_df.write.mode.return_value.partitionBy.return_value.parquet.assert_called_once_with(
        "data/silver"
    )

    quality_validator.validate.assert_called_once_with(written_df)
    mock_write_manifest.assert_called_once()


def test_should_not_block_silver_write_when_quality_fails(mocker):
    spark = mocker.Mock()

    validator = mocker.Mock()
    transformer = mocker.Mock()
    quality_validator = mocker.Mock()

    raw_df = mocker.Mock()
    written_df = mocker.Mock()
    silver_df = mocker.Mock()

    spark.read.parquet.side_effect = [raw_df, written_df]
    transformer.transform.return_value = silver_df
    quality_validator.validate.side_effect = RuntimeError("quality error")

    job = BuildSilverJob(
        spark=spark,
        validator=validator,
        transformer=transformer,
        quality_validator=quality_validator,
    )

    job.execute(
        raw_path="data/raw",
        silver_path="data/silver",
    )

    silver_df.write.mode.return_value.partitionBy.return_value.parquet.assert_called_once_with(
        "data/silver"
    )
    quality_validator.validate.assert_called_once_with(written_df)
