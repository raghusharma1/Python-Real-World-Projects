import pytest
import json
from mock_kaggle_bottle import datasets_list
from bottle import HTTPResponse, request
from unittest.mock import Mock, patch

class Test_MockKaggleBottleDatasetsList:
    @patch('bottle.request.query.page', new_callable=Mock)
    def test_datasets_list_for_first_page(self, mock_query):
        mock_query.return_value = '1'
        response = datasets_list("name")

        assert isinstance(response, HTTPResponse)
        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "application/json"
        assert json.loads(response.body) == [{'title': 'example1'}, {'title': 'example2'}]

    @patch('bottle.request.query.page', new_callable=Mock)
    def test_datasets_list_for_busy_server(self, mock_query):
        mock_query.return_value = '2'
        response = datasets_list("name")

        assert isinstance(response, HTTPResponse)
        assert response.status_code == 429
        assert response.headers.get("Retry-After") == '30'

    @patch('bottle.request.query.page', new_callable=Mock)
    def test_datasets_list_for_nonexistent_pages(self, mock_query):
        mock_query.return_value = '3'
        response = datasets_list("name")

        assert isinstance(response, HTTPResponse)
        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "application/json"
        assert json.loads(response.body) == []
