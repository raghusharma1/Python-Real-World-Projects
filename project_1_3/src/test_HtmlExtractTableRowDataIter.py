# Imports
from urllib.request import urlopen
from bs4 import BeautifulSoup, Tag
from collections.abc import Iterator
from html_extract import table_row_data_iter
import pytest

# Test Class
class Test_HtmlExtractTableRowDataIter:

    @pytest.mark.regression
    def test_iter_with_data_table(self):
        html = """
            <table>
                <tbody>
                    <tr><td>A1</td><td>B1</td></tr>
                    <tr><td>A2</td><td>B2</td></tr>
                </tbody>
            </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        iterator = table_row_data_iter(soup.table)
        result = list(iterator)

        assert result == [["A1", "B1"], ["A2", "B2"]]

    @pytest.mark.edge
    def test_iter_with_empty_table(self):
        html = "<table></table>"
        soup = BeautifulSoup(html, 'html.parser')
        iterator = table_row_data_iter(soup.table)
        result = list(iterator)

        assert result == []

    @pytest.mark.edge
    def test_iter_with_header_only_table(self):
        html = """
            <table>
                <thead><tr><th>Header 1</th><th>Header 2</th></tr></thead>
            </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        iterator = table_row_data_iter(soup.table)
        result = list(iterator)

        assert result == []

    @pytest.mark.regression
    def test_iter_with_nested_table(self):
        html = """
            <table>
                <tbody>
                    <tr><td>A1</td><td><table><tbody><tr><td>Nested</td></tr></tbody></table></td></tr>
                </tbody>
            </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        iterator = table_row_data_iter(soup.table)
        result = list(iterator)

        assert result == [["A1", "Nested"]]

    @pytest.mark.regression
    def test_iter_with_merged_cells_table(self):
        html = """
            <table>
                <tbody>
                    <tr><td colspan="2">A1</td></tr>
                    <tr><td>A2</td><td>B2</td></tr>
                </tbody>
            </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        iterator = table_row_data_iter(soup.table)
        result = list(iterator)

        assert result == [["A1", "A1"], ["A2", "B2"]]
