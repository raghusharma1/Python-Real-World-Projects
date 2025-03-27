import pytest
import sqlite3
import model
from typing import Any
from collections.abc import Iterator
from db_extract import series_iter
from unittest.mock import Mock, MagicMock

class Test_ExtractSeriesIter:

    @pytest.mark.regression
    def test_correct_series_generation(self):
        # Arrange
        mock_conn = Mock(sqlite3.Connection)
        mock_config = {'query': {'names': "SELECT name FROM table"}}
        mock_data = [("name1", ), ("name2", )]
        mock_samples1 = [model.Sample(timestamp=1, value=10), model.Sample(timestamp=2, value=20)]
        mock_samples2 = [model.Sample(timestamp=1, value=30), model.Sample(timestamp=2, value=40)]
        mock_conn.execute.return_value = mock_data
        series_iter = MagicMock()
        series_iter.build_samples.side_effect = [mock_samples1, mock_samples2]

        # Act
        result = list(series_iter(mock_conn, mock_config))

        # Assert
        assert len(result) == 2
        assert result[0].name == mock_data[0][0]
        assert result[0].samples == mock_samples1
        assert result[1].name == mock_data[1][0]
        assert result[1].samples == mock_samples2

    @pytest.mark.regression
    def test_empty_rows(self):
        # Arrange
        mock_conn = Mock(sqlite3.Connection)
        mock_config = {'query': {'names': "SELECT name FROM table"}}
        mock_conn.execute.return_value = []
        series_iter = MagicMock()

        # Act
        result = list(series_iter(mock_conn, mock_config))

        # Assert
        assert len(result) == 0

    @pytest.mark.regression
    def test_database_operation_errors(self):
        # Arrange
        mock_conn = Mock(sqlite3.Connection)
        mock_config = {'query': {'names': "SELECT name FROM table"}}
        mock_conn.execute.side_effect = sqlite3.OperationalError("Database Operation Error")
        series_iter = MagicMock()

        # Act & Assert
        with pytest.raises(sqlite3.OperationalError):
            list(series_iter(mock_conn, mock_config))
