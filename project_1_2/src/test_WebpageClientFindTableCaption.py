import pytest
from bs4 import BeautifulSoup, Tag
from webpage_client import find_table_caption

class Test_WebpageClientFindTableCaption:

    @pytest.mark.valid
    def test_find_table_caption_with_valid_caption(self):
        html = "<table><caption>Anscombe's quartet</caption><tr><td>Test data</td></tr></table>"
        soup = BeautifulSoup(html, 'html.parser')
        result = find_table_caption(soup, "Anscombe's quartet")
        assert isinstance(result, Tag)
        assert result.caption.text.strip() == "Anscombe's quartet"

    @pytest.mark.invalid
    def test_find_table_caption_with_invalid_caption(self):
        html = "<table><caption>Test caption</caption><tr><td>Test data</td></tr></table>"
        soup = BeautifulSoup(html, 'html.parser')
        with pytest.raises(RuntimeError) as exc_info:
            find_table_caption(soup, "Anscombe's quartet")
        assert "with caption 'Anscombe's quartet' not found" in str(exc_info.value)

    @pytest.mark.valid
    def test_find_table_caption_with_multiple_tables(self):
        html = """ <table><caption>Test caption 1</caption><tr><td>Test data 1</td></tr></table>
                   <table><caption>Anscombe's quartet</caption><tr><td>Test data 2</td></tr></table>
                   <table><caption>Test caption 3</caption><tr><td>Test data 3</td></tr></table>"""
        soup = BeautifulSoup(html, 'html.parser')
        result = find_table_caption(soup, "Anscombe's quartet")
        assert isinstance(result, Tag)
        assert result.caption.text.strip() == "Anscombe's quartet"
