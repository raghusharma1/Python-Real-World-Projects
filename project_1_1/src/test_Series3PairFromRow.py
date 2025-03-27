import pytest
from model import RawData
from abc import ABC, abstractmethod
import csv
from pathlib import Path
from unittest.mock import Mock, sentinel, call

class Test_Series3PairFromRow:

    def test_from_row_less_than_four_size(self):
        pair_builder = Mock(spec=PairBuilder)  # creating mock object of PairBuilder 
        pair_builder.target_class = sentinel.some_class 

        with pytest.raises(IndexError):  # Expecting the error
            pair_builder.from_row(["0", "1", "2"])
            
    def test_from_row_success(self):
        pair_builder = Mock(spec=PairBuilder)
        pair_builder.target_class = RawData  # mock target_class

        row = ["0", "1", "2", "3", "4"]
        result = pair_builder.from_row(row)

        assert isinstance(result, RawData)  # Check that result is a RawData
        assert result.first == "0"  # Check if values are assigned correctly
        assert result.fourth == "3"
        
    def test_from_row_non_string_elements(self):
        pair_builder = Mock(spec=PairBuilder)
        pair_builder.target_class = RawData 

        row = [0, 1, 2, 3, 4]
        result = pair_builder.from_row(row)

        assert isinstance(result, RawData)
        assert result.first == "0"
        assert result.fourth == "3"

    def test_from_row_empty_list(self):
        pair_builder = Mock(spec=PairBuilder)
        pair_builder.target_class = RawData

        with pytest.raises(IndexError):  # Expecting the error
            pair_builder.from_row([])

