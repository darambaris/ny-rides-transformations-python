from ny_rides.jobs.build_silver import BuildSilverJob


def test_should_build_silver_layer(mocker):
    spark = mocker.Mock()

    validator = mocker.Mock()
    transformer = mocker.Mock()

    raw_df = mocker.Mock()
    silver_df = mocker.Mock()

    spark.read.parquet.return_value = raw_df

    transformer.transform.return_value = silver_df

    job = BuildSilverJob(
        spark=spark,
        validator=validator,
        transformer=transformer,
    )

    job.execute(
        raw_path="data/raw",
        silver_path="data/silver",
    )

    validator.validate.assert_called_once_with(
        raw_df
    )

    transformer.transform.assert_called_once_with(
        raw_df
    )

    silver_df.write.mode.assert_called_once_with(
        "overwrite"
    )

    silver_df.write.mode.return_value.partitionBy.assert_called_once_with(
        "pickup_year",
        "pickup_month",
    )

    silver_df.write.mode.return_value.partitionBy.return_value.parquet.assert_called_once_with(
        "data/silver"
    )