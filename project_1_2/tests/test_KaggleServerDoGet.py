import pytest
import urllib.parse
from mock_kaggle_server import KaggleServer
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import json
from pathlib import Path
import zipfile
import csv

class Test_KaggleServerDoGet:

    def test_do_GET_page_requests(self):
        server = HTTPServer(('127.0.0.1', 8080), KaggleServer)
        response_page_1 = server.do_GET(urllib.parse.urlparse("/api/v1/datasets/list?page=1"))
        response_page_2 = server.do_GET(urllib.parse.urlparse("/api/v1/datasets/list?page=2"))
        response_page_other = server.do_GET(urllib.parse.urlparse("/api/v1/datasets/list?page=3"))
        assert response_page_1.status_code == 200
        assert response_page_1.headers["Content-Type"] == "application/json"
        assert json.loads(response_page_1.text) == [{'title': 'example1'}, {'title': 'example2'}]
        assert response_page_2.status_code == 429
        assert response_page_other.status_code == 200
        assert response_page_other.headers["Content-Type"] == "application/json"
        assert json.loads(response_page_other.text) == []

    def test_do_GET_dataset_download(self):
        server = HTTPServer(('127.0.0.1', 8080), KaggleServer)
        response_valid_dataset = server.do_GET(urllib.parse.urlparse("/api/v1/datasets/download/carlmcbrideellis/data-anscombes-quartet"))
        response_invalid_dataset = server.do_GET(urllib.parse.urlparse("/api/v1/datasets/download/invalid_dataset"))
        assert response_valid_dataset.status_code == 200
        assert response_valid_dataset.headers["Content-Type"] == "application/zip"
        assert zipfile.is_zipfile(io.BytesIO(response_valid_dataset.content))
        assert response_invalid_dataset.status_code == 404

    def test_do_GET_dataset_metadata(self):
        server = HTTPServer(('127.0.0.1', 8080), KaggleServer)
        response_valid_dataset = server.do_GET(urllib.parse.urlparse("/api/v1/datasets/metadata/carlmcbrideellis/data-anscombes-quartet"))
        response_invalid_dataset = server.do_GET(urllib.parse.urlparse("/api/v1/datasets/metadata/invalid_dataset"))
        assert response_valid_dataset.status_code == 200
        assert response_valid_dataset.headers["Content-Type"] == "application/json"
        assert json.loads(response_valid_dataset.text) == {"name": "Data: Anscombe's quartet"}
        assert response_invalid_dataset.status_code == 404

    def test_do_GET_unknown_path(self):
        server = HTTPServer(('127.0.0.1', 8080), KaggleServer)
        response_unknown_path = server.do_GET(urllib.parse.urlparse("/unknown_path"))
        assert response_unknown_path.status_code == 404
