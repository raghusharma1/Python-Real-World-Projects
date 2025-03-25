import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path
import sys
import pytest
from csv_extract import main
from unittest.mock import patch, Mock, mock_open

class Test_AcquireMain:

    @pytest.mark.valid
    @patch('csv_extract.get_options')
    @patch('csv_extract.EXTRACT_CLASS')
    @patch('csv_extract.BUILDER_CLASSES')
    @patch('csv_extract.Path.open')
    @patch('csv_extract.csv.reader')
    def test_main_valid_inputs(self, mock_csv_reader, mock_path_open, mock_builder, mock_extract, mock_get_options):
        mock_argv = ['arg1', 'arg2', 'arg3']
        mock_get_options.return_value = mock_argv
        mock_path_open.return_value = mock_open(read_data="data")
        mock_build_pairs = Mock()
        mock_extract.return_value.build_pairs.return_value = mock_build_pairs

        # Execution
        main(['arg1', 'arg2', 'arg3'])

        # Assertions
        mock_get_options.assert_called_once_with(mock_argv)
        mock_path_open.assert_called()
        mock_csv_reader.assert_called_with(mock_path_open())
        mock_build_pairs.assert_called_with(csv.reader(mock_path_open()))

    @pytest.mark.negative
    @patch('csv_extract.get_options')
    def test_main_no_source_files(self, mock_get_options):
        mock_argv = ['arg1', 'arg2']
        mock_get_options.return_value = mock_argv

        # Execution
        main(['arg1', 'arg2'])

        # Assertions
        mock_get_options.assert_called_once_with(mock_argv)

    @pytest.mark.invalid
    @patch('csv_extract.get_options')
    @patch('csv_extract.Path')
    def test_main_no_output_dir(self, mock_path, mock_get_options):
        mock_argv = ['arg1', 'arg2', 'arg3']
        mock_get_options.return_value = mock_argv
        mock_path.return_value = None

        with pytest.raises(Exception):
            main(['arg1', 'arg2', 'arg3'])

    @pytest.mark.invalid
    @patch('csv_extract.get_options')
    @patch('csv_extract.csv.reader')
    def test_main_invalid_csv(self, mock_csv_reader, mock_get_options):
        mock_argv = ['arg1', 'arg2', 'arg3']
        mock_get_options.return_value = mock_argv
        mock_csv_reader.side_effect = csv.Error()

        with pytest.raises(csv.Error):
            main(['arg1', 'arg2', 'arg3'])
