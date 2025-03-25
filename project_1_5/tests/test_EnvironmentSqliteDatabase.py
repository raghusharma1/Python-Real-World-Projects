import pytest
from collections.abc import Iterator
from pathlib import Path
import shutil
import sqlite3
from tempfile import mkdtemp
from behave import fixture, use_fixture
from behave.runner import Context
import tomllib
from environment import sqlite_database

class Test_EnvironmentSqliteDatabase:
    @pytest.mark.regression
    def test_checkout_and_rollback_of_schema(self):
        # Arrange
        context =  Context("mock")
        context.schema = "schema_data"

        # Act
        database = sqlite_database(context)

        # Assert
        assert isinstance(database, Iterator), "Failed to create database iterator"
        assert context.connection is not None, "Failed to open database connection"
        assert not context.working_path.exists(), "Failed to delete working path"

    @pytest.mark.negative
    def test_failure_in_config_loading(self):
        # Arrange
        context =  Context("mock")
        context.config_path = "non_existent_file.toml"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            sqlite_database(context)

    @pytest.mark.security  
    def test_sql_injection_handling(self):
        # Arrange
        context =  Context("mock")
        context.config_path = " malicious_sql_config.toml" # contains sql injection

        # Assert
        with pytest.raises(sqlite3.OperationalError): 
            sqlite_database(context) # should throw an error due to SQL Injection

    @pytest.mark.regression
    def test_database_closure(self):
        # Arrange
        context =  Context("mock")
        context.manipulation_sql = "CREATE TABLE faulty_table" # faulty manipulation sql

        # Act
        sqlite_database(context)

        # Assert
        assert not context.connection, "Unexpected database connection found"
        assert not context.working_path.exists(), "Failed to delete working path"

