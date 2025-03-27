import pytest
from model import RawData
from unittest.mock import Mock, sentinel
from csv_extract import from_row

class Test_Series4PairFromRow:

    @pytest.mark.valid
    def test_from_row_rawdata_creation(self):
        # Arrange
        list_of_values = ['value1', 'value2', 'value3', 'value4', 'value5', 'value6'] 
        mock_cls = Mock(return_value=sentinel.RawData)
        row = Mock()
        row.target_class = mock_cls

        # Act
        result = from_row(row, list_of_values)

        # Assert
        mock_cls.assert_called_once_with('value5', 'value6')
        assert result == sentinel.RawData

    @pytest.mark.invalid
    def test_from_row_rawdata_insufficient_values(self):
        # Arrange
        list_of_values = ['value1', 'value2', 'value3'] 
        mock_cls = Mock(return_value=sentinel.RawData)
        row = Mock()
        row.target_class = mock_cls

        # Act_Asert
        with pytest.raises(IndexError):
            from_row(row, list_of_values)

    @pytest.mark.valid
    def test_from_row_target_class_assignment(self):
        # Arrange
        list_of_values = ['value1', 'value2', 'value3', 'value4', 'value5', 'value6']
        mock_cls = Mock(return_value=sentinel.RawData)
        row = Mock()
        row.target_class = mock_cls

        # Act
        result = from_row(row, list_of_values)

        # Assert
        assert isinstance(result, sentinel.RawData)
        assert row.target_class is mock_cls

    @pytest.mark.invalid
    def test_from_row_invalid_target_class(self):
        # Arrange
        list_of_values = ['value1', 'value2', 'value3', 'value4', 'value5', 'value6']
        mock_cls = Mock(side_effect=TypeError())
        row = Mock()
        row.target_class = mock_cls

        # Act_Asert
        with pytest.raises(TypeError):
            from_row(row, list_of_values)
