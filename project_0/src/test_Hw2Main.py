import pytest
import sys
from hw2 import main

class Test_Hw2Main:
    @pytest.mark.regression
    def test_main_no_args(self):
        try:
            main()
        except Exception as e:
            pytest.fail(f"Unexpected Exception {e}")

    @pytest.mark.regression
    def test_main_with_args(self):
        test_args = ['arg1', 'arg2']
        old_args = sys.argv
        sys.argv = ['', *test_args]

        try:
            main()
        except Exception as e:
            pytest.fail(f"Unexpected Exception {e}")

        sys.argv = old_args
        
    @pytest.mark.regression
    def test_main_with_empty_sysargv(self):
        old_args = sys.argv
        sys.argv = ['']

        try:
            main()
        except Exception as e:
            pytest.fail(f"Unexpected Exception {e}")

        sys.argv = old_args

    @pytest.mark.regression
    def test_main_with_invalid_arg_format(self):
        invalid_args = ['--invalidarg']
        old_args = sys.argv
        sys.argv = ['', *invalid_args]
        
        with pytest.raises(Exception):  # Replace Exception with appropriate exception class
            main()

        sys.argv = old_args
