import pytest
from unittest.mock import Mock, call
from collections.abc import Iterator
from typing import Any
from environment import before_tag, kaggle_server
from behave.runner import Context

class Test_EnvironmentBeforeTag:
    
    @pytest.mark.regression
    def test_before_tag_with_kaggle_server_tag(self):
        context = Mock(Context)
        tag = "fixture.kaggle_server"
        with pytest.raises(StopIteration):
            before_tag(context, tag)
        context.mock_calls == [call.use_fixture(kaggle_server, context)] 
    
    @pytest.mark.negative
    def test_before_tag_with_non_kaggle_server_tag(self):
        context = Mock(Context)
        tag = "fixture.non_kaggle_server"
        with pytest.raises(StopIteration):
            before_tag(context, tag)
        assert not context.mock_calls   
        
    @pytest.mark.negative
    def test_before_tag_with_null_tag(self):
        context = Mock(Context)
        tag = ""
        with pytest.raises(StopIteration):
            before_tag(context, tag)
        assert not context.mock_calls
