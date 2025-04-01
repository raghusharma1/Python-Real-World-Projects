import pytest
from hello_world import greeting
from io import StringIO
import sys

class Test_HelloWorldGreeting:

    @pytest.mark.positive
    def test_default_greeting(self, capsys):
        greeting() 
        captured = capsys.readouterr()
        assert captured.out == "Hello, World!\n"

    @pytest.mark.positive
    def test_specified_greeting(self, capsys):
        test_name = "John"
        greeting(test_name) 
        captured = capsys.readouterr()
        assert captured.out == f"Hello, {test_name}!\n"

    @pytest.mark.negative
    def test_greeting_special_characters(self, capsys):
        test_name = "@$#%"
        greeting(test_name) 
        captured = capsys.readouterr()
        assert captured.out == f"Hello, {test_name}!\n"

    @pytest.mark.negative
    def test_empty_user_greeting(self, capsys):
        test_name = ""
        greeting(test_name) 
        captured = capsys.readouterr()
        assert captured.out == "Hello, !\n"
