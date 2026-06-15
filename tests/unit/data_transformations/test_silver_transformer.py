from ny_rides.contracts.yellow_taxi_contract import YellowTaxiContract
from ny_rides.data_transformations.silver_transformer import SilverTransformer


class FakeExpr:
    def alias(self, _name):
        return self

    def cast(self, _dtype):
        return self

    def __sub__(self, _other):
        return self

    def __truediv__(self, _other):
        return self


def test_should_select_required_columns(mocker):
    dataframe = mocker.Mock()
    silver_df = mocker.Mock()

    dataframe.select.return_value = silver_df
    silver_df.withColumn.return_value = silver_df

    mocker.patch(
        "ny_rides.data_transformations.silver_transformer.col",
        return_value=FakeExpr(),
    )
    mocker.patch(
        "ny_rides.data_transformations.silver_transformer.year",
        return_value=FakeExpr(),
    )
    mocker.patch(
        "ny_rides.data_transformations.silver_transformer.month",
        return_value=FakeExpr(),
    )
    mocker.patch(
        "ny_rides.data_transformations.silver_transformer.unix_timestamp",
        return_value=FakeExpr(),
    )

    transformer = SilverTransformer()

    transformer.transform(dataframe)

    dataframe.select.assert_called_once_with(*YellowTaxiContract.REQUIRED_COLUMNS)


def test_should_apply_expected_enrichment_columns(mocker):
    dataframe = mocker.Mock()
    silver_df = mocker.Mock()
    silver_df_with_partitions = mocker.Mock()

    dataframe.select.return_value = silver_df
    silver_df.select.return_value = silver_df_with_partitions
    silver_df_with_partitions.withColumn.return_value = silver_df_with_partitions
    silver_df.withColumn.return_value = silver_df

    mocker.patch(
        "ny_rides.data_transformations.silver_transformer.col",
        return_value=FakeExpr(),
    )
    mocker.patch(
        "ny_rides.data_transformations.silver_transformer.year",
        return_value=FakeExpr(),
    )
    mocker.patch(
        "ny_rides.data_transformations.silver_transformer.month",
        return_value=FakeExpr(),
    )
    mocker.patch(
        "ny_rides.data_transformations.silver_transformer.unix_timestamp",
        return_value=FakeExpr(),
    )

    transformer = SilverTransformer()

    result = transformer.transform(dataframe)

    assert result == silver_df_with_partitions

    initial_added_columns = [
        call.args[0] for call in silver_df.withColumn.call_args_list
    ]

    final_added_columns = [
        call.args[0] for call in silver_df_with_partitions.withColumn.call_args_list
    ]

    assert "VendorID" in initial_added_columns
    assert "total_amount" in initial_added_columns
    assert "trip_duration_minutes" in final_added_columns
