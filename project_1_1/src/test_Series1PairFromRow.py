import pytest
from model import RawData, XYPair
from abc import ABC, abstractmethod
import csv
from pathlib import Path
from unittest.mock import Mock, sentinel, call
from csv_extract import from_row

class Test_Series1PairFromRow:

    @pytest.fixture
    def target_class(self):
        return Series1Pair

    @pytest.mark.positive
    def test_instance_initialization(self, target_class):
        row = ['value1', 'value2']

        result_instance = target_class.from_row(row)

        assert isinstance(result_instance, RawData)
        assert result_instance.value1 == 'value1'
        assert result_instance.value2 == 'value2'

    @pytest.mark.negative
    @pytest.mark.parametrize("row", [
        ['value1', 'value2', 'value3'],
        ['value1', 'value2', 'value3', 'value4']
    ])
    def test_too_many_row_values(self, target_class, row):
        with pytest.raises(ValueError) as e:
            target_class.from_row(row)
        assert str(e.value) == 'Too many values to unpack'

    @pytest.mark.negative
    def test_empty_row_values(self, target_class):
        row = []
        with pytest.raises(ValueError) as e:
            target_class.from_row(row)
        assert str(e.value) == 'Not enough values to unpack'
