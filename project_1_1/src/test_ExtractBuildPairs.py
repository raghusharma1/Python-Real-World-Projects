import pytest
from model import RawData, XYPair
from abc import ABC, abstractmethod
import csv
from pathlib import Path
from unittest.mock import Mock, sentinel, call
from csv_extract import build_pairs

class Test_ExtractBuildPairs():

    def test_build_pairs_normal(self):
        mock_bldr_1 = Mock()
        mock_bldr_2 = Mock()
        mock_bldrs = [mock_bldr_1, mock_bldr_2]
        row = ['test', 'data']
        
        expected_result = [mock_bldr_1.from_row.return_value, mock_bldr_2.from_row.return_value]
        instance = EXTRACT_CLASS(mock_bldrs)
        
        result = instance.build_pairs(row)
        
        for bldr in mock_bldrs:
            bldr.from_row.assert_called_once_with(row)
        assert result == expected_result

    def test_build_pairs_empty_row(self):
        mock_bldr_1 = Mock()
        mock_bldr_2 = Mock()
        mock_bldrs = [mock_bldr_1, mock_bldr_2]
        row = []
        
        expected_result = []
        instance = EXTRACT_CLASS(mock_bldrs)
        
        result = instance.build_pairs(row)
        
        for bldr in mock_bldrs:
            bldr.from_row.assert_called_once_with(row)
        assert result == expected_result

    def test_build_pairs_non_standard_builder(self):
        mock_bldr_1 = Mock()
        mock_bldr_2 = Mock()
        mock_bldr_ns = Mock() # Non-standard PairBuilder
        mock_bldrs = [mock_bldr_1, mock_bldr_2, mock_bldr_ns]
        row = ['test', 'data']
        
        expected_result = [mock_bldr_1.from_row.return_value, mock_bldr_2.from_row.return_value, mock_bldr_ns.from_row.return_value]
        instance = EXTRACT_CLASS(mock_bldrs)
        
        result = instance.build_pairs(row)
        
        for bldr in mock_bldrs:
            bldr.from_row.assert_called_once_with(row)
        assert result == expected_result
