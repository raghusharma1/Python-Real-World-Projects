import pytest
import argparse
import sys
from hw import get_options

class Test_HwGetOptions:

    def test_command_line_handling(self):
        """Verify that the function handles command-line arguments as intended"""
        test_args = ['arg1', 'arg2', 'arg3']
        res = get_options(test_args)
        assert isinstance(res, argparse.Namespace), "The result should be an instance of argparse.Namespace"
        assert res.__dict__ == {'arg1': True, 'arg2': True, 'arg3': True}

    def test_common_options(self):
        """Test the function with common command-line options or flag"""
        test_args = ['--version', '-h']
        res = get_options(test_args)
        assert isinstance(res, argparse.Namespace), "The result should be an instance of argparse.Namespace"
        assert res.__dict__ == {'version': True, 'help': True}

    def test_no_options(self):
        """Test the function with missing command-line options"""
        test_args = []
        try:
            res = get_options(test_args)
            assert isinstance(res, argparse.Namespace), "The result should be an instance of argparse.Namespace"
        except argparse.ArgumentError:
            pytest.fail("get_options function failed because no arguments were provided")

    def test_long_option_with_equals(self):
        """Validate the function's ability to handle long options with '=' sign"""
        test_args = ['--arg1=value1', '--arg2=value2']
        res = get_options(test_args)
        assert isinstance(res, argparse.Namespace), "The result should be an instance of argparse.Namespace"
        assert res.__dict__ == {'arg1': 'value1', 'arg2': 'value2'}
