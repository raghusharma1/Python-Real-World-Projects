import pytest
import html_extract
import logging
from acquire import dump_table
from unittest.mock import patch

class Test_AcquireDumpTable:
    
    @patch('acquire.html_extract.get_page')
    @patch('acquire.html_extract.find_table_caption')
    @patch('acquire.html_extract.table_row_data_iter')
    def test_dump_table_valid_url_caption(self, mock_data_iter, mock_find_caption, mock_get_page):
        mock_get_page.return_value = 'valid_page_content'
        mock_find_caption.return_value = 'valid_table_tag'
        mock_data_iter.side_effect = [['empty_line'], ['header_line'], ['row1', 'row2']]

        dump_table('http://validurl.com', 'valid_caption')
        mock_get_page.assert_called_once_with('http://validurl.com')
        mock_find_caption.assert_called_once_with('valid_page_content', 'valid_caption')
        assert mock_data_iter.call_count == 1

    @patch('acquire.html_extract.get_page')
    def test_dump_table_invalid_url(self, mock_get_page):
        mock_get_page.side_effect = Exception('Invalid URL')
        
        with pytest.raises(Exception) as e_info:
            dump_table('http://invalidurl.com', 'random_caption')
        assert str(e_info.value) == 'Invalid URL'

    @patch('acquire.html_extract.get_page')
    @patch('acquire.html_extract.find_table_caption')
    def test_dump_table_missing_caption(self, mock_find_caption, mock_get_page):
        mock_get_page.return_value = 'valid_page_content'
        mock_find_caption.return_value = None

        with pytest.raises(RuntimeError) as re_info:
            dump_table('http://validurl.com', 'missing_caption')
        assert 'Table not found' in str(re_info.value)

    @patch('acquire.html_extract.get_page')
    @patch('acquire.html_extract.find_table_caption')
    @patch('acquire.html_extract.table_row_data_iter')
    def test_dump_table_no_table_data(self, mock_data_iter, mock_find_caption, mock_get_page):
        mock_get_page.return_value = 'valid_page_content'
        mock_find_caption.return_value = 'valid_table_tag'
        mock_data_iter.side_effect = [['empty_line'], ['header_line']]

        dump_table('http://validurl.com', 'valid_caption')
        mock_get_page.assert_called_once_with('http://validurl.com')
        mock_find_caption.assert_called_once_with('valid_page_content', 'valid_caption')
        assert mock_data_iter.call_count == 1
