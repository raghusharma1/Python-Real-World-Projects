import pytest
import argparse
import sys
from io import StringIO
from contextlib import redirect_stdout
from hello_world import main

# Test Class
class Test_HelloWorldMain:

    @pytest.mark.regression
    def test_should_use_world_as_default_greeting_value(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ['prog'])
        f = StringIO()
        with redirect_stdout(f):
            main()
        out = f.getvalue()
        assert out == 'Hello, World!\n'

    @pytest.mark.regression
    def test_should_greet_custom_name_when_provided(self, monkeypatch):
        test_name = "TestName"
        monkeypatch.setattr(sys, 'argv', ['prog', '--who', test_name])
        f = StringIO()
        with redirect_stdout(f):
            main()
        out = f.getvalue()
        assert out == f'Hello, {test_name}!\n'

    @pytest.mark.regression
    def test_should_ignore_additional_arguments(self, monkeypatch):
        test_name = "TestName"
        monkeypatch.setattr(sys, 'argv', ['prog', '--who', test_name, '--unsupported', 'arg'])
        f = StringIO()
        with redirect_stdout(f):
            main()
        out = f.getvalue()
        assert out == f'Hello, {test_name}!\n'

    @pytest.mark.regression
    def test_should_properly_parse_from_list_of_arguments(self, monkeypatch):
        test_name = "TestName"
        argv_list = ['prog', '-w', test_name]
        monkeypatch.setattr(sys, 'argv', argv_list)
        f = StringIO()
        with redirect_stdout(f):
            main()
        out = f.getvalue()
        assert out == f'Hello, {test_name}!\n'
