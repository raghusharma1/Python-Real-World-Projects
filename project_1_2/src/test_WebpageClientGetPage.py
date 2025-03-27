import pytest
from urllib.error import URLError
from bs4 import BeautifulSoup
from webpage_client import get_page


class Test_WebpageClientGetPage:

    @pytest.mark.valid
    def test_get_page_with_valid_url(self):
        # Arrange
        valid_url = 'https://www.example.com'  # TODO: change to a valid url

        # Act
        returned_bs4_obj = get_page(valid_url)

        # Assert
        assert isinstance(returned_bs4_obj, BeautifulSoup)

    @pytest.mark.invalid
    def test_get_page_with_invalid_url(self):
        # Arrange
        invalid_url = 'http://www.non-existent-website.xxx'  # TODO: Change to an invalid url

        # Assert
        with pytest.raises(URLError):
            # Act
            get_page(invalid_url)

    @pytest.mark.invalid
    def test_get_page_with_non_html_content_url(self):
        # Arrange
        non_html_content_url = 'http://example.com/test_image.jpg'  # TODO: Change to url pointing non-HTML content

        # Assert
        with pytest.raises(ValueError):
            # Act
            get_page(non_html_content_url)

    @pytest.mark.security
    def test_get_page_with_authentication_required_url(self):
        # Arrange
        authentication_required_url = 'https://www.example.com/login'  # TODO: Change to url requiring user authentication

        # Assert
        with pytest.raises(URLError):
            # Act
            get_page(authentication_required_url)
