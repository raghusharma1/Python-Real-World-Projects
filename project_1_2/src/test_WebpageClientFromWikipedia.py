import pytest
from webpage_client import from_wikipedia
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup, Tag
from urllib.request import urlopen
from collections.abc import Iterator

class Test_WebpageClientFromWikipedia:
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_wikipedia_page_availability(self):
        with patch('urllib.request.urlopen') as mock_urlopen:
            from_wikipedia()
            mock_urlopen.assert_called_once_with("https://en.wikipedia.org/wiki/Anscombe%27s_quartet")

    @pytest.mark.regression
    def test_find_table_caption(self):
        mock_tag = Mock(Tag)
        mock_soup = Mock(BeautifulSoup)
        mock_soup.find = Mock(return_value=mock_tag)
        caption = "Anscombe's quartet"

        with patch('webpage_client.find_table_caption', return_value=mock_tag) as mock_find_table_caption:
            mock_find_table_caption(mock_soup, caption)
            mock_soup.find.assert_called_with('caption', text=caption)

    @pytest.mark.regression
    def test_extract_rows(self):
        fake_table = BeautifulSoup('<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>', 'html.parser')
        expected_output = [("1", "2"), ("3", "4")]

        with patch('webpage_client.extract_rows', return_value=expected_output) as mock_extract_rows:
            output = mock_extract_rows(fake_table)
            assert output == expected_output

    @pytest.mark.valid
    @pytest.mark.negative
    def test_no_table_existence(self):
        mock_soup = Mock(BeautifulSoup)
        mock_soup.find = Mock(return_value=None)
        caption = "Anscombe's quartet"

        with patch('webpage_client.find_table_caption') as mock_find_table_caption:
            with patch('webpage_client.from_wikipedia') as mock_from_wikipedia:
                mock_find_table_caption.return_value = None
                mock_from_wikipedia.return_value = None
                assert mock_from_wikipedia() == None
