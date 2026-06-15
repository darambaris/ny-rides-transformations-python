from ny_rides.quality.quality_validator import QualityValidator


class TestFailurePercentage:
    """Tests for QualityValidator._failure_percentage method."""

    def test_should_return_zero_when_failed_rows_is_zero(self):
        result = QualityValidator._failure_percentage(0, 100)
        assert result == 0.0

    def test_should_return_zero_when_total_rows_is_zero(self):
        result = QualityValidator._failure_percentage(10, 0)
        assert result == 0.0

    def test_should_return_none_when_failed_rows_is_none(self):
        result = QualityValidator._failure_percentage(None, 100)
        assert result is None

    def test_should_calculate_percentage_correctly(self):
        result = QualityValidator._failure_percentage(50, 1000)
        assert result == 5.0

    def test_should_round_to_4_decimals(self):
        result = QualityValidator._failure_percentage(1, 3)
        assert result == 33.3333

    def test_should_handle_small_percentages(self):
        result = QualityValidator._failure_percentage(1, 100000)
        assert result == 0.001

    def test_should_handle_large_percentages(self):
        result = QualityValidator._failure_percentage(999, 1000)
        assert result == 99.9

    def test_should_handle_100_percent_failure(self):
        result = QualityValidator._failure_percentage(1000, 1000)
        assert result == 100.0
