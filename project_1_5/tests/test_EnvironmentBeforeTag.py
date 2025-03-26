import pytest
from collections.abc import Iterator
from pathlib import Path
import shutil
import sqlite3
from tempfile import mkdtemp
from behave import fixture, use_fixture
from behave.runner import Context
import tomllib
import toml as tomllib
from environment import before_tag

class Test_EnvironmentBeforeTag:
    
    @pytest.fixture(autouse=True)
    def mock_sqlite_database_fixture(self, monkeypatch):
        class MockedFixture:
            def __init__(self):
                self.invoked = False
            
            def __enter__(self):
                self.invoked = True
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                pass
            
        mocked_fixture = MockedFixture()
        monkeypatch.setattr(Path('environment.before_tag'), 'sqlite_database', mocked_fixture)  # Make sure the path corresponds to your path
        yield mocked_fixture

    def test_fixture_sqlite_tag_invocation(self, mock_sqlite_database_fixture):
        context = Context(None)
        tag = 'fixture.sqlite'
        
        before_tag(context, tag)
        
        assert mock_sqlite_database_fixture.invoked is True
    
    def test_nonfixture_sqlite_tag_invocation(self, mock_sqlite_database_fixture):
        context = Context(None)
        tag = 'fixture.non_sqlite'
        
        before_tag(context, tag)
        
        assert mock_sqlite_database_fixture.invoked is False
    
    def test_null_tag_invocation(self, mock_sqlite_database_fixture):
        context = Context(None)
        tag = None
        
        before_tag(context, tag)
        
        assert mock_sqlite_database_fixture.invoked is False

    def test_context_as_null_invocation(self, mock_sqlite_database_fixture):
        context = None
        tag = 'fixture.sqlite'
        
        with pytest.raises(AttributeError):
            before_tag(context, tag)
            
        assert mock_sqlite_database_fixture.invoked is False
