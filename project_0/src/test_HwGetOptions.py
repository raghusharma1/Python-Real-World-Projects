import argparse
import sys
import pytest
from hw import get_options

class Test_HwGetOptions:

    def test_get_options_no_args(self):
        assert isinstance(get_options([]), argparse.Namespace)

    def test_get_options_valid_args(self):
        valid_args = ['arg1', 'arg2', 'arg3']

        result = get_options(valid_args)

        assert isinstance(result, argparse.Namespace)
        assert result.arg1 == 'arg1'
        assert result.arg2 == 'arg2'
        assert result.arg3 == 'arg3'

    def test_get_options_invalid_args(self):
        invalid_args = ['invalid_arg1', 'invalid_arg2', 'invalid_arg3']

        with pytest.raises((SystemExit, ValueError)):
            get_options(invalid_args)

    def test_get_options_large_amount_args(self):
        large_amount_of_args = ['arg{}'.format(i) for i in range(1000)]

        result = get_options(large_amount_of_args)

        assert isinstance(result, argparse.Namespace)
        for i in range(1000):
            assert hasattr(result, 'arg{}'.format(i))
