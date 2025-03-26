import pytest
from unittest.mock import Mock
import logging
from importlib import import_module
from kaggle_client import RestAccess

class Test_RestAccessErrorDump:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.log_capture_string = io.StringIO()
        self.ch = logging.StreamHandler(self.log_capture_string)
        self.ch.setLevel(logging.DEBUG)
        RestAccess.logger.addHandler(self.ch)
        self.ra = RestAccess()

    @pytest.mark.regular
    def test_error_dump_logs_all_headers(self):
        mock_response = Mock()
        mock_response.headers.items.return_value = {'header1': 'value1', 'header2': 'value2'}
        self.ra.error_dump('prefix', mock_response)
        log_contents = self.log_capture_string.getvalue()
        assert 'header1' in log_contents
        assert 'header2' in log_contents

    @pytest.mark.regular
    def test_error_dump_shortens_long_headers(self):
        long_header_string = ''.join('a' for _ in range(129))
        mock_response = Mock()
        mock_response.headers.items.return_value = {'header1': long_header_string}
        self.ra.error_dump('prefix', mock_response)
        log_contents = self.log_capture_string.getvalue()
        assert len(log_contents.split(':')[1].strip()) == 128

    @pytest.mark.regular
    def test_error_dump_logs_request_details(self):
        mock_response = Mock()
        mock_response.request.method = 'GET'
        mock_response.request.url = 'http://example.com'
        self.ra.error_dump('prefix', mock_response)
        log_contents = self.log_capture_string.getvalue()
        assert mock_response.request.method in log_contents
        assert mock_response.request.url in log_contents

    @pytest.mark.regular
    def test_error_dump_logs_response_content(self):
        mock_response = Mock()
        mock_response.content = 'Some response content'
        self.ra.error_dump('prefix', mock_response)
        log_contents = self.log_capture_string.getvalue()
        assert mock_response.content in log_contents 
