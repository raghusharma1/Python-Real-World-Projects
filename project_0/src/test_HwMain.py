import pytest
import sys
from hw import main

class Test_HwMain:
    
    @pytest.mark.regression
    def test_main_without_arguments(self):
        with pytest.raises(SystemExit):
            main([])

    @pytest.mark.regression
    def test_main_with_valid_arguments(self):
        assert main(["-h"]) == None
    
    @pytest.mark.negative
    def test_main_with_invalid_arguments(self):
        with pytest.raises(SystemExit):
            main(["-i"])

    @pytest.mark.negative
    def test_main_with_excessive_arguments(self):
        with pytest.raises(SystemExit):
            main(["-h"] * 1000)
