import pytest
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections.abc import Iterator
from html_extract import get_page

class Test_HtmlExtractGetPage:

    @pytest.mark.valid
    @pytest.mark.regression
    def test_get_page_valid_url(self):
        # Arrange
        valid_url = "https://en.wikipedia.org"  # TODO: Replace with a valid URL

        # Act
        result = get_page(valid_url)

        # Assert
        assert isinstance(result, BeautifulSoup)

    @pytest.mark.invalid
    @pytest.mark.negative
    def test_get_page_invalid_url(self):
        # Arrange
        invalid_url = "htps:/en.wikipedia"  # TODO: Replace with a invalid URL

        # Act
        with pytest.raises(ValueError):
            get_page(invalid_url)

    @pytest.mark.edge
    @pytest.mark.negative
    def test_get_page_no_html(self):
        # Arrange
        no_html_url = "https://example.com/no_html"  # TODO: Replace with a URL which has no HTML

        # Act
        result = get_page(no_html_url)

        # Assert
        assert result is None  # Assuming function returns None for no HTML content

    @pytest.mark.performance
    @pytest.mark.negative
    def test_get_page_no_internet(self):
        # Arrange
        valid_url = "https://en.wikipedia.org"  # TODO: Validate no internet access before running the test

        # Act
        with pytest.raises(Exception):  # Expecting generic Exception on internet connectivity issue, replace with specific Exception if required
            get_page(valid_url)

    @pytest.mark.security
    @pytest.mark.negative
    def test_get_page_ssl_issue(self):
        # Arrange
        ssl_issue_url = "https://self-signed.badssl.com/"  # TODO: Replace with a URL with SSL certificate issues

        # Act
        with pytest.raises(Exception):  # Expecting generic Exception on SSL issue, replace with specific Exception if required
            get_page(ssl_issue_url)
