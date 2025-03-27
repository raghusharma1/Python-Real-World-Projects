import subprocess
import shlex
from pathlib import Path
import pytest
from unittest.mock import Mock
from hw_cli import step_impl

# Test class 
class Test_HwCliStepImpl:
    
    # Test function for scenario 1
    def test_step_impl_successful_run(self, mocker):
        # Arrange: Setting up a mock context object
        mock_context = Mock()
        mock_context.status.returncode = 0
        mock_context.output = 'output'
        
        # Act: Calling the function to test
        step_impl(mock_context, 'output')

    # Test function for scenario 2
    def test_step_impl_unsuccessful_run(self, mocker):
        # Arrange: Setting up a mock context object for a failed subprocess call
        mock_context = Mock()
        mock_context.status.returncode = 1
        mock_context.output = 'output'
        
        # Act and Assert: Expect an assertion error to be raised
        with pytest.raises(AssertionError):
            step_impl(mock_context, 'output')

    # Test function for scenario 3
    def test_step_impl_missing_expected_output(self, mocker):
        # Arrange: Setting up a mock context object where output doesn't match
        mock_context = Mock()
        mock_context.status.returncode = 0
        mock_context.output = 'different output'
        
        # Act and Assert: Expect an assertion error to be raised
        with pytest.raises(AssertionError):
            step_impl(mock_context, 'output')