import pytest
from unittest.mock import Mock, patch
from kaggle_client import RestAccess
from requests.models import Response

class Test_RestAccessGetPagedJson:

    @pytest.mark.parametrize('url, query', [('http://test_url.com', {'key': 'value'})])
    @patch('requests.get')
    def test_valid_request(self, mock_get, url, query):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'value'}
        mock_get.return_value = mock_response
        rest_access = RestAccess({'username': 'test', 'key': 'test'})
        result = list(rest_access.get_paged_json(url, query))
        mock_get.assert_called_once_with(url, params={'key': 'value', 'page': '1'}, headers={"Accept": "application/json"}, auth=rest_access.credentials)
        assert result == [{'data': 'value'}]

    @pytest.mark.parametrize('url, query, responses', [('http://test_url.com', None, [{'data1': 'value1'}, {'data2': 'value2'}])])
    @patch('requests.get')
    def test_paged_request(self, mock_get, url, query, responses):
        mock_responses = [Mock(spec=Response) for _ in responses]
        for resp, data in zip(mock_responses, responses):
            resp.status_code = 200
            resp.json.return_value = data
        mock_get.side_effect = mock_responses
        rest_access = RestAccess({'username': 'test', 'key': 'test'})
        result = list(rest_access.get_paged_json(url, query))
        expected_calls = [((url, {'params': {'page': str(i+1)}, 'headers': {"Accept": "application/json"}, 'auth': rest_access.credentials}),)
                          for i in range(len(responses))]
        assert mock_get.call_args_list == expected_calls
        assert result == responses

    @pytest.mark.parametrize('url, query', [('http://test_url.com', {'key': 'value'})])
    @patch('requests.get')
    def test_no_data(self, mock_get, url, query):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        rest_access = RestAccess({'username': 'test', 'key': 'test'})
        result = list(rest_access.get_paged_json(url, query))
        mock_get.assert_called_once_with(url, params={'key': 'value', 'page': '1'}, headers={"Accept": "application/json"}, auth=rest_access.credentials)
        assert result == []

    @pytest.mark.parametrize('url, query', [('http://test_url.com', {'key': 'value'})])
    @patch('requests.get')
    def test_error_response(self, mock_get, url, query):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 429
        mock_response.json.return_value = {'error': 'Too many requests'}
        mock_get.return_value = mock_response
        rest_access = RestAccess({'username': 'test', 'key': 'test'})
        with pytest.raises(SystemExit):
            list(rest_access.get_paged_json(url, query))
        mock_get.assert_called_once_with(url, params={'key': 'value', 'page': '1'}, headers={"Accept": "application/json"}, auth=rest_access.credentials)

    @pytest.mark.parametrize('url, query, responses', [('http://test_url.com', None, [{'data1': 'value1'}, {'data2': 'value2'}, {'data3': 'value3'}])])
    @patch('requests.get')
    def test_multi_page_iteration(self, mock_get, url, query, responses):
        mock_responses = [Mock(spec=Response) for _ in responses]
        for resp, data in zip(mock_responses, responses):
            resp.status_code = 200
            resp.json.return_value = data
        mock_get.side_effect = mock_responses
        rest_access = RestAccess({'username': 'test', 'key': 'test'})
        result = list(rest_access.get_paged_json(url, query))
        expected_calls = [((url, {'params': {'page': str(i+1)}, 'headers': {"Accept": "application/json"}, 'auth': rest_access.credentials}),)
                          for i in range(len(responses))]
        assert mock_get.call_args_list == expected_calls
        assert result == responses
