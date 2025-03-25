# Required Imports
import pytest
from collections.abc import Iterator
from typing import Any
import subprocess
import time
import os
import sys
from behave import fixture, use_fixture
from behave.runner import Context
from environment import kaggle_server

# Test Class
class Test_EnvironmentKaggleServer:

    def test_start_server(self):
        context = Context()
        server = kaggle_server(context)
        assert isinstance(server, Iterator), "Server subprocess failed to start"
    
    def test_server_killing(self):
        context = Context()
        server = kaggle_server(context)
        next(server) 
        server.close()
        with pytest.raises(StopIteration):
            next(server), "Server subprocess continues running after killing"
        
    def test_environment_setting(self):
        context = Context()
        server = kaggle_server(context)
        next(server) 
        assert context.environment["ACQUIRE_BASE_URL"] == "http://127.0.0.1:8080", "Environment setting failed"
    
    def test_delay_verification(self):
        context = Context()
        start_time = time.time()
        server = kaggle_server(context)
        end_time = time.time()
        next(server) 
        assert end_time - start_time >= 0.5, "Built-in delay is less than 0.5s"
