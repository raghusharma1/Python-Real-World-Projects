import os
import pytest
import argparse
from acquire import get_options

class Test_AcquireGetOptions:

    @pytest.mark.positive
    def test_get_options_valid_arguments(self):
        os.environ["ACQUIRE_BASE_URL"] = "http://test.com"
        test_argv = ["-o", "/path/to/output", "-k", "/path/to/key", "-z", "zip_Data", "-b", "http://test.com"]
        result = get_options(test_argv)
        assert result.output == "/path/to/output"
        assert result.key == "/path/to/key"
        assert result.zip == "zip_Data"
        assert result.baseurl == "http://test.com"

    @pytest.mark.negative
    def test_get_options_missing_optional_arguments(self):
        os.environ["ACQUIRE_BASE_URL"] = "http://test.com"
        test_argv = ["-o", "/path/to/output"]
        result = get_options(test_argv)
        assert result.output == "/path/to/output"
        assert result.key is None
        assert result.zip == "carlmcbrideellis/data-anscombes-quartet"
        assert result.baseurl == "http://test.com"

    @pytest.mark.negative
    def test_get_options_invalid_arguments(self):
        os.environ["ACQUIRE_BASE_URL"] = "http://test.com"
        invalid_test_argv = ["-o", "/path/to/output", "-x"]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            get_options(invalid_test_argv)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 2

    @pytest.mark.negative
    def test_get_options_no_env_variable(self):
        if "ACQUIRE_BASE_URL" in os.environ:
            del os.environ["ACQUIRE_BASE_URL"]
        test_argv = ["-o", "/path/to/output"]
        result = get_options(test_argv)
        assert result.output == "/path/to/output"
        assert result.baseurl == "https://www.kaggle.com"
