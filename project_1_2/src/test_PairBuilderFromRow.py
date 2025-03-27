import pytest
from kaggle_client import PairBuilder, RawData

class Test_PairBuilderFromRow:
    
    @pytest.mark.positive
    def test_successful_from_row_conversion(self):
        # Arrange
        row = ['sample_data_1', 'sample_data_2', 'sample_data_3']
        builder = PairBuilder()

        # Act
        result = builder.from_row(row)

        # Assert
        assert isinstance(result, RawData)
        assert result.value_1 == 'sample_data_1'
        assert result.value_2 == 'sample_data_2'
        assert result.value_3 == 'sample_data_3'

    @pytest.mark.negative
    def test_incorrect_row_length(self):
        # Arrange
        row = ['sample_data_1', 'sample_data_2']
        builder = PairBuilder()

        # Act
        with pytest.raises(Exception):
            builder.from_row(row)

    @pytest.mark.negative
    def test_empty_row(self):
        # Arrange
        row = []
        builder = PairBuilder()

        # Act
        with pytest.raises(Exception):
            builder.from_row(row)

    @pytest.mark.regular
    def test_special_character_handling(self):
        # Arrange
        row = ['sample_data_1!', 'sample_data_2@', 'sample_data_3#']
        builder = PairBuilder()

        # Act
        result = builder.from_row(row)

        # Assert
        assert isinstance(result, RawData)
        assert result.value_1 == 'sample_data_1!'
        assert result.value_2 == 'sample_data_2@'
        assert result.value_3 == 'sample_data_3#'
