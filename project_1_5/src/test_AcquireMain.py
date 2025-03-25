import argparse
import sys
from unittest import mock
import pytest
import csv
import sqlite3
import toml
from typ import Any
from os import Path
from unittest.mock import patch
from acquire import main

class Test_AcquireMain:

    # Scenario 1: Test the file read operation of the configuration file
    @pytest.mark.parametrize('filepath', ['tempfile.toml'])
    @patch.object(toml, "load", autospec=True)
    @patch.object(argparse.Namespace, "schema", autospec=True)
    def test_file_read_operation(self, mock_open, mock_load, filepath):
        options = argparse.Namespace()
        options.schema = Path(filepath)
        main([])
        mock_open.assert_called_with('rb')
        mock_load.assert_called()

    # Scenario 2: Database connection establishment and validation
    @patch.object(sqlite3, "connect", autospec=True)
    @patch.object(argparse.Namespace, "__init__", return_value=None)
    def test_db_connection(self, mock_db_uri, mock_connect):
        options = argparse.Namespace()
        options.db_uri = 'test:uri'
        main([])
        mock_connect.assert_called_with(options.db_uri, uri=True)

    # Scenario 3: Iteration of series from a Database
    @patch.object(Extract, "series_iter", return_value=[mock.MagicMock()])
    @patch.object(sqlite3, "connect", autospec=True)
    @patch.object(argparse.Namespace, "__init__", return_value=None)
    def test_series_iteration(self, mock_db_uri, mock_connect, mock_series_iter):
        options = argparse.Namespace()
        options.db_uri = 'test:uri'
        main([])
        mock_series_iter.assert_called()

    # Scenario 4: Validation of CSV File creation and data writing
    @patch.object(csv.DictWriter, "writeheader", autospec=True)
    @patch.object(csv.DictWriter, "writerows", autospec=True)
    def test_csv_generation(self, mock_writeheader, mock_writerows):
        options = argparse.Namespace()
        target = (options.output / "name").with_suffix(".csv")
        with target.open('w', newline='') as output_file:
            writer = csv.DictWriter(output_file, ['x', 'y'])
            writer.writeheader()
            writer.writerows(
                [{'x': "sample.x", 'y': "sample.y"}]
            )
        mock_writerows.assert_called()
        mock_writeheader.assert_called()

    # Scenario 5: Test the exception when no URI provided
    @pytest.mark.parametrize('uri', ['', None, '   '])
    @patch.object(argparse.Namespace, "__init__", return_value=None)
    def test_no_uri_exception(self, mock_db_uri, uri):
        options = argparse.Namespace()
        options.db_uri = uri
        with pytest.raises(RuntimeError):
            main([])
