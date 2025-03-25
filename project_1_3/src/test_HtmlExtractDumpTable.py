import pytest
from urllib.request import urlopen
from bs4 import BeautifulSoup, Tag
from collections.abc import Iterator
from html_extract import dump_table

class Test_HtmlExtractDumpTable:
    """
    Class for testing dump_table function with different test scenarios.
    """

    @pytest.mark.regression
    def test_dump_table_valid_url_caption(self, mocker):
        """
        Scenario 1: Correct URL and Caption
        """
        mocker.patch('urlopen', return_value='<html><body><table></table></body></html>')
        mocker.patch('BeautifulSoup', return_value=BeautifulSoup('<table><tr><td>data</td></tr></table>', 'html.parser'))

        # TODO: Replace with valid URL and caption
        url = "valid_url"
        table_caption = "correct_caption"

        result = dump_table(url, table_caption)
        assert result == ['data'], "Test Case Fails. Function did not return correct table data."

    @pytest.mark.negative
    def test_dump_table_missing_caption(self, mocker):
        """
        Scenario 2: Missing Table Caption in the URL
        """
        mocker.patch('urlopen', return_value='<html><body><table></table></body></html>')
        mocker.patch('BeautifulSoup', return_value=BeautifulSoup('<table></table>', 'html.parser'))

        # TODO: Replace with valid URL and incorrect caption
        url = "valid_url"
        table_caption = "incorrect_caption"

        with pytest.raises(ValueError):
            result = dump_table(url, table_caption)


    @pytest.mark.invalid
    def test_dump_table_unreachable_url(self):
        """
        Scenario 3: Unreachable URL
        """
        # TODO: Replace with invalid/unreachable URL and caption
        url = "unreachable_url"
        table_caption = "random_caption"

        with pytest.raises(Exception):
            result = dump_table(url, table_caption)


    @pytest.mark.negative
    def test_dump_table_no_table_data(self, mocker):
        """
        Scenario 4: Iterating over Empty Table Data
        """
        mocker.patch('urlopen', return_value='<html><body><table></table></body></html>')
        mocker.patch('BeautifulSoup', return_value=BeautifulSoup('<table></table>', 'html.parser'))

        # TODO: Replace with valid URL and caption that refers to an empty table
        url = "valid_url"
        table_caption = "empty_table_caption"

        result = dump_table(url, table_caption)
        assert result is None, "Test Case Fails. Function did not handle empty table case correctly."
