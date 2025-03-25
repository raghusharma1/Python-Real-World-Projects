import pytest
import argparse
import logging
from pathlib import Path
import sys
from acquire import main

class Test_AcquireMain:
    @pytest.mark.regular
    def test_main_no_arguments(self, monkeypatch):
        test_args = []
        monkeypatch.setattr(sys, 'argv', test_args)
        with pytest.raises(SystemExit):
            main()

    @pytest.mark.regular
    def test_main_with_arguments(self, monkeypatch):
        test_args = ['app.py', '-p', 'test_page', '-c', 'test_caption']
        monkeypatch.setattr(sys, 'argv', test_args)
        with pytest.raises(SystemExit):
            main()

    @pytest.mark.invalid
    def test_main_invalid_arguments(self, monkeypatch):
        test_args = ['app.py', '-p', 'test_page', '-c']
        monkeypatch.setattr(sys, 'argv', test_args)
        with pytest.raises(SystemExit):
            main()

    @pytest.mark.output
    def test_main_dump_table(self, monkeypatch, caplog):
        test_args = ['app.py', '-p', 'test_page', '-c', 'test_caption']
        monkeypatch.setattr(sys, 'argv', test_args)
        caplog.set_level(logging.INFO)
        with pytest.raises(SystemExit):
            main()
        assert 'Finished writing info to test_page' in caplog.text

    @pytest.mark.error
    def test_main_nonexistent_page(self, monkeypatch, caplog):
        test_args = ['app.py', '-p', 'test_page_nonexistent', '-c', 'test_caption']
        monkeypatch.setattr(sys, 'argv', test_args)
        caplog.set_level(logging.ERROR)
        with pytest.raises(SystemExit):
            main()
        assert 'Failed to fetch info from test_page_nonexistent' in caplog.text
