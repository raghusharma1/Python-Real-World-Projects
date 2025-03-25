import pytest
import argparse
import csv
import json
import logging
import os
import sys
import zipfile
from pathlib import Path
from unittest.mock import Mock, patch
from model import *
from kaggle_client import RestAccess
from acquire import main

logger = logging.getLogger('acquire')

class Test_AcquireMain:

    @pytest.mark.positive
    def test_successful_data_downloading(self):
        with patch('acquire.RestAccess') as mock_RestAccess, \
             patch('args.Namespace') as mock_Namespace, \
             patch('{}'.format(logger.name)) as mock_logger, \
             patch('acquire.get_options') as mock_get_options:

            mock_RestAccess.get_zip.return_value = zipfile.Zipfile()
            mock_Namespace.key = Path('key.json')
            mock_Namespace.baseurl = "https://www.test.com"
            mock_Namespace.zip = "test_zip.zip"
            mock_get_options.return_value = mock_Namespace

            main()

            mock_logger.info.assert_called_with("Downloading %s", "https://www.test.com/api/v1/datasets/download/test_zip.zip")

    @pytest.mark.negative
    def test_fail_data_downloading_no_credentials(self):
        with patch('acquire.get_options') as mock_get_options, \
             patch('{}'.format(logger.name)) as mock_logger:

            mock_Namespace = Mock()
            mock_Namespace.key = None
            mock_get_options.return_value = mock_Namespace

            with pytest.raises(SystemExit) as pytest_wrapped_e:
                main()

            mock_logger.error.assert_called_with("No credentials file provided on command line.")
            assert pytest_wrapped_e.type == SystemExit
            assert pytest_wrapped_e.value.code == 2

    @pytest.mark.positive
    def test_successful_extraction_of_csv_from_zip(self):
        with patch('acquire.RestAccess') as mock_RestAccess, \
             patch('csv.DictReader') as mock_DictReader, \
             patch('args.Namespace') as mock_Namespace, \
             patch('{}'.format(logger.name)) as mock_logger, \
             patch('acquire.get_options') as mock_get_options:

            mock_RestAccess.get_zip.return_value = zipfile.Zipfile()
            mock_Namespace.key = Path('key.json')
            mock_Namespace.baseurl = "https://www.test.com"
            mock_Namespace.zip = "test_zip.zip"
            mock_Namespace.namelist.return_value = ['Anscombe_quartet_data.csv']
            mock_get_options.return_value = mock_Namespace

            main()
            
            mock_logger.info.assert_called_with("Opening %s", "Anscombe_quartet_data.csv")

    @pytest.mark.negative
    def test_handle_csv_not_found_in_zip(self):
        with patch('acquire.RestAccess') as mock_RestAccess, \
             patch('args.Namespace') as mock_Namespace, \
             patch('{}'.format(logger.name)) as mock_logger, \
             patch('acquire.get_options') as mock_get_options:

            mock_RestAccess.get_zip.return_value = zipfile.Zipfile()
            mock_Namespace.key = Path('key.json')
            mock_Namespace.baseurl = "https://www.test.com"
            mock_Namespace.zip = "test_zip.zip"
            mock_Namespace.namelist.return_value = []
            mock_get_options.return_value = mock_Namespace

            main()
            
            mock_logger.error.assert_called_with("Could not find %s in %s", "Anscombe_quartet_data.csv", [] )
