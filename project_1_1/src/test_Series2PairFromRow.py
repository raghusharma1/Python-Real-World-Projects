import pytest
from model import RawData, XYPair
from abc import ABC, abstractmethod
import csv
from pathlib import Path
from unittest.mock import Mock, sentinel, call
from csv_extract import from_row

class Test_Series2PairFromRow:

    @pytest.mark.positive
    @pytest.mark.regression
    def test_from_row_normal_execution(self):
        # Arrange
        mock_cls = Mock(return_value=sentinel.expected_result)
        target_class = mock_cls
        test_row = ["Element1", "Element2", "Element3"]

        # Act
        result = from_row(target_class, test_row)

        # Assert
        assert result == sentinel.expected_result
        mock_cls.assert_called_once_with("Element1", "Element3")

    @pytest.mark.negative
    @pytest.mark.regression
    def test_from_row_insufficient_data(self):
        # Arrange
        mock_cls = Mock()
        target_class = mock_cls
        test_row = ["Element"]

        # Act & Assert
        with pytest.raises(IndexError):
            from_row(target_class, test_row)

    @pytest.mark.positive
    @pytest.mark.regression
    def test_from_row_with_non_String_elements(self):
        # Arrange
        mock_cls = Mock(return_value=sentinel.expected_result)
        target_class = mock_cls
        test_row = [1, 2, 3]

        # Act
        result = from_row(target_class, test_row)

        # Assert
        assert result == sentinel.expected_result
        mock_cls.assert_called_once_with(1, 3)