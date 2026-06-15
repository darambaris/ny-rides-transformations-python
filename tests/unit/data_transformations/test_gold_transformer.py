from ny_rides.data_transformations.gold_transformer import GoldTransformer


def test_should_group_by_pickup_year_and_month(mocker):
    dataframe = mocker.Mock()
    grouped = mocker.Mock()
    aggregated = mocker.Mock()
    ordered = mocker.Mock()

    dataframe.groupBy.return_value = grouped
    grouped.agg.return_value = aggregated
    aggregated.orderBy.return_value = ordered

    mocker.patch("ny_rides.data_transformations.gold_transformer.F")

    transformer = GoldTransformer()
    result = transformer.build_monthly_average_total_amount(dataframe)

    dataframe.groupBy.assert_called_once_with("pickup_year", "pickup_month")
    grouped.agg.assert_called_once()
    aggregated.orderBy.assert_called_once_with("pickup_year", "pickup_month")
    assert result is ordered


def test_should_return_dataframe_from_monthly_average(mocker):
    dataframe = mocker.Mock()
    grouped = mocker.Mock()
    aggregated = mocker.Mock()
    ordered = mocker.Mock()

    dataframe.groupBy.return_value = grouped
    grouped.agg.return_value = aggregated
    aggregated.orderBy.return_value = ordered

    mocker.patch("ny_rides.data_transformations.gold_transformer.F")

    transformer = GoldTransformer()
    result = transformer.build_monthly_average_total_amount(dataframe)

    assert result is ordered


def test_should_add_pickup_hour_column(mocker):
    dataframe = mocker.Mock()
    with_hour = mocker.Mock()
    grouped = mocker.Mock()
    aggregated = mocker.Mock()
    ordered = mocker.Mock()

    dataframe.withColumn.return_value = with_hour
    with_hour.groupBy.return_value = grouped
    grouped.agg.return_value = aggregated
    aggregated.orderBy.return_value = ordered

    mock_f = mocker.patch("ny_rides.data_transformations.gold_transformer.F")
    mock_f.hour.return_value = "pickup_hour_expr"

    transformer = GoldTransformer()
    transformer.build_hourly_average_passenger_count(dataframe)

    dataframe.withColumn.assert_called_once_with("pickup_hour", "pickup_hour_expr")
    mock_f.hour.assert_called_once_with("tpep_pickup_datetime")


def test_should_group_by_pickup_year_month_and_hour(mocker):
    dataframe = mocker.Mock()
    with_hour = mocker.Mock()
    grouped = mocker.Mock()
    aggregated = mocker.Mock()
    ordered = mocker.Mock()

    dataframe.withColumn.return_value = with_hour
    with_hour.groupBy.return_value = grouped
    grouped.agg.return_value = aggregated
    aggregated.orderBy.return_value = ordered

    mocker.patch("ny_rides.data_transformations.gold_transformer.F")

    transformer = GoldTransformer()
    transformer.build_hourly_average_passenger_count(dataframe)

    with_hour.groupBy.assert_called_once_with(
        "pickup_year", "pickup_month", "pickup_hour"
    )
    grouped.agg.assert_called_once()
    aggregated.orderBy.assert_called_once_with(
        "pickup_year", "pickup_month", "pickup_hour"
    )


def test_should_return_dataframe_from_hourly_average(mocker):
    dataframe = mocker.Mock()
    with_hour = mocker.Mock()
    grouped = mocker.Mock()
    aggregated = mocker.Mock()
    ordered = mocker.Mock()

    dataframe.withColumn.return_value = with_hour
    with_hour.groupBy.return_value = grouped
    grouped.agg.return_value = aggregated
    aggregated.orderBy.return_value = ordered

    mocker.patch("ny_rides.data_transformations.gold_transformer.F")

    transformer = GoldTransformer()
    result = transformer.build_hourly_average_passenger_count(dataframe)

    assert result is ordered
