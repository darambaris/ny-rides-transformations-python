from ny_rides.jobs.build_gold import BuildGoldJob


def test_should_build_monthly_and_hourly_datasets(mocker):
    spark = mocker.Mock()
    transformer = mocker.Mock()

    silver_df = mocker.Mock()
    monthly_df = mocker.Mock()
    hourly_df = mocker.Mock()

    spark.read.parquet.return_value = silver_df
    transformer.build_monthly_average_total_amount.return_value = monthly_df
    transformer.build_hourly_average_passenger_count.return_value = hourly_df

    monthly_df.count.return_value = 9
    hourly_df.count.return_value = 24

    job = BuildGoldJob(spark=spark, transformer=transformer)
    job.execute(silver_path="data/silver", gold_path="data/gold")

    spark.read.parquet.assert_called_once_with("data/silver")
    transformer.build_monthly_average_total_amount.assert_called_once_with(silver_df)
    transformer.build_hourly_average_passenger_count.assert_called_once_with(silver_df)


def test_should_write_monthly_dataset_to_correct_path(mocker):
    spark = mocker.Mock()
    transformer = mocker.Mock()

    silver_df = mocker.Mock()
    monthly_df = mocker.Mock()
    hourly_df = mocker.Mock()

    spark.read.parquet.return_value = silver_df
    transformer.build_monthly_average_total_amount.return_value = monthly_df
    transformer.build_hourly_average_passenger_count.return_value = hourly_df

    job = BuildGoldJob(spark=spark, transformer=transformer)
    job.execute(silver_path="data/silver", gold_path="data/gold")

    monthly_df.write.mode.assert_called_once_with("overwrite")
    monthly_df.write.mode.return_value.parquet.assert_called_once_with(
        "data/gold/monthly_average_total_amount"
    )


def test_should_write_hourly_dataset_to_correct_path(mocker):
    spark = mocker.Mock()
    transformer = mocker.Mock()

    silver_df = mocker.Mock()
    monthly_df = mocker.Mock()
    hourly_df = mocker.Mock()

    spark.read.parquet.return_value = silver_df
    transformer.build_monthly_average_total_amount.return_value = monthly_df
    transformer.build_hourly_average_passenger_count.return_value = hourly_df

    job = BuildGoldJob(spark=spark, transformer=transformer)
    job.execute(silver_path="data/silver", gold_path="data/gold")

    hourly_df.write.mode.assert_called_once_with("overwrite")
    hourly_df.write.mode.return_value.parquet.assert_called_once_with(
        "data/gold/hourly_average_passenger_count"
    )


def test_should_use_custom_gold_path(mocker):
    spark = mocker.Mock()
    transformer = mocker.Mock()

    silver_df = mocker.Mock()
    monthly_df = mocker.Mock()
    hourly_df = mocker.Mock()

    spark.read.parquet.return_value = silver_df
    transformer.build_monthly_average_total_amount.return_value = monthly_df
    transformer.build_hourly_average_passenger_count.return_value = hourly_df

    job = BuildGoldJob(spark=spark, transformer=transformer)
    job.execute(silver_path="data/silver", gold_path="custom/gold")

    monthly_df.write.mode.return_value.parquet.assert_called_once_with(
        "custom/gold/monthly_average_total_amount"
    )
    hourly_df.write.mode.return_value.parquet.assert_called_once_with(
        "custom/gold/hourly_average_passenger_count"
    )
