import pytest
from urllib.parse import urlparse
from pathlib import Path
import json
import subprocess
import shlex
from cli_interface import step_impl

class Test_CliInterfaceStepImpl:

    @pytest.mark.regression
    def test_url_substitution(self):
        class Context:
            def __init__(self):    
                self.path = Path('/sample/path/to/file') 
                
        context = Context()      
        expected_url = 'file:///sample/path/to/file'
        expected_command = [
            'python', 'src/acquire.py',
            '-o', 'quartet',
            '--page', expected_url,
            '--caption', "Anscombe's quartet"
        ]
        with capsys.disabled():
            step_impl(context)
        captured = capsys.readouterr()
        assert shlex.split(captured.out) == expected_command 
        

    @pytest.mark.regression
    def test_path_handling(self):
        class Context:    
            def __init__(self, path):    
                self.path = Path(path)     

        context1 = Context('/absolute/path/to/file')
        context2 = Context('relative/path/to/file')

        expected_url1 = 'file:///absolute/path/to/file'
        expected_url2 = 'file://relative/path/to/file'

        with capsys.disabled():
            step_impl(context1)
        captured1 = capsys.readouterr()
        
        with capsys.disabled():
            step_impl(context2)
        captured2 = capsys.readouterr()

        assert expected_url1 in captured1.out   
        assert expected_url2 in captured2.out   
        

    @pytest.mark.regression
    def test_command_creation(self):
        class Context:
            def __init__(self):    
                self.path = Path('/sample/path/to/file')
                
        context = Context()
        expected_command = [
            'python', 'src/acquire.py',
            '-o', 'quartet',
            '--page', 'file:///sample/path/to/file',
            '--caption', "Anscombe's quartet"
        ]

        with capsys.disabled():
            step_impl(context)
        captured = capsys.readouterr()

        assert shlex.split(captured.out) == expected_command 
