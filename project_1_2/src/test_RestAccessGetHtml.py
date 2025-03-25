import pytest
from unittest.mock import Mock, patch
from kaggle_client import RestAccess

class Test_RestAccessGetHtml:
    @pytest.mark.positive
    def test_get_html_success(self):
        mock_requests = Mock()
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.headers = {"Content-Type": "text/html"}
        response_mock.content = b'<html>Hello, World!</html>'
        mock_requests.get.return_value = response_mock

        with patch("kaggle_client.requests", new=mock_requests):
            rest_client = RestAccess({'username': 'test', 'key': 'test-key'})
            url = 'http://test.com'
            params = {"param1": "value1"}
            result = rest_client.get_html(url, params)

        mock_requests.get.assert_called_once_with(url, auth=rest_client.credentials, params=params, headers={"Accept": "text/html"})
        assert result == b'<html>Hello, World!</html>'

    @pytest.mark.negative
    def test_get_html_404(self):
        mock_requests = Mock()
        response_mock = Mock()
        response_mock.status_code = 404
        mock_requests.get.return_value = response_mock

        with patch("kaggle_client.requests", new=mock_requests):
            rest_client = RestAccess({'username': 'test', 'key': 'test-key'})
            url = 'http://test.com/404'
            params = {"param1": "value1"}

            with pytest.raises(Exception, match="UNEXPECTED"):
                rest_client.get_html(url, params)

        mock_requests.get.assert_called_once_with(url, auth=rest_client.credentials, params=params, headers={"Accept": "text/html"})

    @pytest.mark.negative
    def test_get_html_non_html_mime_type(self):
        mock_requests = Mock()
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.headers = {"Content-Type": "application/json"}
        mock_requests.get.return_value = response_mock

        with patch("kaggle_client.requests", new=mock_requests):
            rest_client = RestAccess({'username': 'test', 'key': 'test-key'})
            url = 'http://test.com/json'
            
            with pytest.raises(Exception, match="UNEXPECTED"):
                rest_client.get_html(url)

        mock_requests.get.assert_called_once_with(url, auth=rest_client.credentials, headers={"Accept": "text/html"})

    @pytest.mark.positive
    def test_get_html_without_params(self):
        mock_requests = Mock()
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.headers = {"Content-Type": "text/html"}
        response_mock.content = b'<html>Welcome to test.com</html>'
        mock_requests.get.return_value = response_mock
                              
        with patch("kaggle_client.requests", new=mock_requests):
            rest_client = RestAccess({'username': 'test', 'key': 'test-key'})
            url = 'http://test.com'
            result = rest_client.get_html(url)

        mock_requests.get.assert_called_once_with(url, auth=rest_client.credentials, headers={"Accept": "text/html"})
        assert result == b'<html>Welcome to test.com</html>'
