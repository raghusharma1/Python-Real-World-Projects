# Required Libraries 
import pytest
from pathlib import Path
from unittest.mock import Mock
from db_interface import step_impl

# Test Class
class Test_DbInterfaceStepImpl:
    
    # Scenario 1: Valid Output File Presence
    def test_valid_output_file_presence(self, tmp_path):
        dummy_context = Mock()
        dummy_context.working_path = tmp_path
        file = tmp_path / "output_name"
        file.write_text("content")
        
        # No error should be raised for valid file
        step_impl(dummy_context, "output_name")

    # Scenario 2: Invalid Output File Presence
    def test_invalid_output_file_presence(self, tmp_path):
        dummy_context = Mock()
        dummy_context.working_path = tmp_path
        with pytest.raises(AssertionError) as ex:
            step_impl(dummy_context, "non_existent_file")
        assert str(ex.value) == 'No non_existent_file file found'
   
    # Scenario 3: Output Path Points to a directory
    def test_directory_path_instead_of_file(self, tmp_path):
        dummy_context = Mock()
        dummy_context.working_path = tmp_path
        directory = tmp_path / 'output_dir'
        directory.mkdir()
        with pytest.raises(AssertionError) as ex:
            step_impl(dummy_context, "output_dir")
        assert str(ex.value) == 'No output_dir file found'
    
    # Scenario 4: Checking Relative Working Path
    def test_relative_working_path(self, tmp_path):
        relative_path = tmp_path.relative_to(Path.cwd())
        dummy_context = Mock()
        dummy_context.working_path = relative_path
        file = tmp_path / "relative"
        file.write_text("content")
        
        # No error should be raised for valid relative path
        step_impl(dummy_context, "relative")
