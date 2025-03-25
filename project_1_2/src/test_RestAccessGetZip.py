import pytest
import requests
from unittest.mock import Mock, patch
from kaggle_client import RestAccess
import zipfile
import io

class Test_RestAccessGetZip:
    
    @pytest.mark.positive
    def test_get_zip_successful(self):
        # Arrange 
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/zip'}
        mock_response.content = b'some content'
        with patch.object(requests, 'get', return_value=mock_response):
            rest_access = RestAccess({ 'username': 'dummy', 'key': 'key' })

            # Act
            result = rest_access.get_zip('http://test_url')
        
            # Assert
            assert isinstance(result, zipfile.ZipFile)

    @pytest.mark.negative
    def test_get_zip_unsuccessful(self):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 404
        with patch.object(requests, 'get', return_value=mock_response) as mock_get:
            rest_access = RestAccess({ 'username': 'dummy', 'key': 'key' })
            
            # Act
            result = rest_access.get_zip('http://test_url')

            # Assert
            mock_get.assert_called()
            assert result is None
            
    @pytest.mark.negative
    def test_get_zip_non_zip_content(self):
        # Arrange 
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.content = b'{"key": "value"}'
        
        with patch.object(requests, 'get', return_value=mock_response) as mock_get:
            rest_access = RestAccess({ 'username': 'dummy', 'key': 'key' })
            
            # Act
            result = rest_access.get_zip('http://test_url')

            # Assert
            mock_get.assert_called()
            assert result is None