import json
import pytest
from unittest.mock import patch, mock_open
from kaggle_client import main
from pathlib import Path

class Test_KaggleClientMain:
    @pytest.mark.smoke
    def test_load_credentials_from_file(self):
        test_credentials = {"username": "test_user", "key": "test_key"}
        mock_file_path = "fake_path/kaggle.json"
        Path.home = lambda: "fake_path"
        with patch('builtins.open', mock_open(read_data=json.dumps(test_credentials))) as mock_file:
            main()
            mock_file.assert_called_once_with(mock_file_path, 'r')
            
    @pytest.mark.regression
    @patch('kaggle_client.RestAccess')
    def test_data_extraction(self, mock_RestAccess):
        mock_RestAccess.return_value.get_json.return_value = {"testkey": "testvalue"}
        expected_response = {"testkey": "testvalue"}
        url = "https://www.kaggle.com/api/v1/datasets/list"
        response = main(url)
        assert response == expected_response
    
    @pytest.mark.valid
    @patch('kaggle_client.RestAccess')
    def test_retrieve_dataset(self, mock_RestAccess):
        test_datasets = [
            {'title': 'Not Anscombe', 'ref': '/path/not_anscombe', 'url': '/not_anscombe', 'totalBytes': 500},
            {'title': 'Anscombe', 'ref': '/path/anscombe', 'url': '/anscombe', 'totalBytes': 1000}
        ]
        mock_RestAccess.return_value.get_paged_json.return_value = test_datasets
        main()
        assert main.data_ref == '/path/anscombe'
        assert main.data_url == '/anscombe'
        
    @pytest.mark.valid
    @patch('kaggle_client.RestAccess')
    def test_extract_metadata(self, mock_RestAccess):
        metadata = {"test_metadata_key": "test_metadata_value"}
        mock_RestAccess.return_value.get_json.return_value = metadata
        metadata_url = 'https://www.kaggle.com/api/v1/datasets/metadata/test_ref'
        main()
        assert main.get_json(metadata_url) == metadata

    @pytest.mark.regression
    @patch('kaggle_client.RestAccess')
    def test_extract_data_from_downloadable_source(self, mock_RestAccess):
        test_file_contents = "column1,column2\nvalue1,value2"
        mock_RestAccess.return_value.get_zip.return_value = test_file_contents
        main()
        assert main.get_zip() == test_file_contents
