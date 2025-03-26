import pytest
from csv_extract import from_row
from model import RawData
from unittest.mock import Mock, sentinel, call

class Test_PairBuilderFromRow:
    @pytest.mark.regression
    def test_correct_transformation(self):
        mock_list = ['item1', 'item2', 'item3', 'item4']
        expected_raw_data = RawData('item1', 'item2', 'item3', 'item4')
        result = from_row(mock_list)
        assert expected_raw_data == result

    @pytest.mark.negative
    def test_empty_input(self):
        with pytest.raises(Exception): # assuming an exception is thrown for empty input
            from_row([])

    @pytest.mark.negative
    def test_non_string_input(self):
        non_string_list = [123, True, 456.789, ['item1', 'item2']]
        with pytest.raises(Exception): # assuming an exception is thrown for non-string input
            from_row(non_string_list)

    @pytest.mark.performance
    def test_large_data(self):
        large_list = ['item']*100000  ### TODO: Adjust as needed
        expected_raw_data = RawData(*large_list)
        result = from_row(large_list)
        assert expected_raw_data == result
