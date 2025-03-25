import pytest
import requests
from unittest.mock import patch, MagicMock
from kaggle_client import RestAccess

class Test_RestAccessGetJson:
    
    @pytest.mark.positive
    def test_successful_get_json_request(self):
        # Arrange 
        url = 'https://test_url.com'
        params = {'param1': 'value1'}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {'test': 'data'}
        # Act
        with patch.object(requests, 'get', return_value=mock_response):
            rest_access = RestAccess({'username':'test', 'key':'test'})
            result = rest_access.get_json(url, params)
        # Assert
        assert result == {'test': 'data'}

    @pytest.mark.negative
    def test_unsuccessful_get_json_due_to_incorrect_content_type(self):
        # Arrange 
        url = 'https://test_url.com'
        params = {'param1': 'value1'}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/html"}
        # Act
        with patch.object(requests, 'get', return_value=mock_response) as mock_get, \
                patch.object(RestAccess, 'error_dump') as mock_error_dump:
            rest_access = RestAccess({'username':'test', 'key':'test'})
            rest_access.get_json(url, params)
        # Assert
        mock_error_dump.assert_called_once_with("NOT application/json", mock_response)

    @pytest.mark.negative
    def test_unsuccessful_get_json_due_to_bad_status_code(self):
        # Arrange 
        url = 'https://test_url.com'
        params = {'param1': 'value1'}
        mock_response = MagicMock()
        mock_response.status_code = 404
        # Act
        with patch.object(requests, 'get', return_value=mock_response) as mock_get, \
                patch.object(RestAccess, 'error_dump') as mock_error_dump:
            rest_access = RestAccess({'username':'test', 'key':'test'})
            rest_access.get_json(url, params)
        # Assert
        mock_error_dump.assert_called_once_with("UNEXPECTED", mock_response)
    
    @pytest.mark.negative
    def test_successful_get_request_but_no_json_returned(self):
        # Arrange 
        url = 'https://test_url.com'
        params = {'param1': 'value1'}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = None
        # Act
        with patch.object(requests, 'get', return_value=mock_response) as mock_get, \
                patch.object(RestAccess, 'error_dump') as mock_error_dump:
            rest_access = RestAccess({'username':'test', 'key':'test'})
            rest_access.get_json(url, params)
        # Assert
        mock_error_dump.assert_called_once()
