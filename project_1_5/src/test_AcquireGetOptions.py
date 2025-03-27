import pytest
from acquire import get_options
from argparse import Namespace
from pathlib import Path

class Test_AcquireGetOptions:

    @pytest.mark.regression
    @pytest.mark.smoke
    def test_missing_arguments(self):
        # Arrange
        argument_list = ['script_name']

        # Act
        result = get_options(argument_list)

        # Assert
        assert result == Namespace(output=None, db_uri="file:example.db", schema=Path("schema.toml"))

    @pytest.mark.regression
    @pytest.mark.valid
    @pytest.mark.positive
    def test_user_arguments(self):
        # Arrange
        argument_list = ['script_name', '-o', 'output_path', '-d', 'database_uri', '-s', 'schema_path']

        # Act
        result = get_options(argument_list)

        # Assert
        assert result == Namespace(output=Path('output_path'), db_uri="database_uri", schema=Path('schema_path'))

    @pytest.mark.regression
    @pytest.mark.invalid
    @pytest.mark.negative
    def test_invalid_path(self):
        # Arrange
        argument_list = ['script_name', '-o', 'invalid_output_path', '-s', 'invalid_schema_path']

        # Act and Assert
        with pytest.raises(FileNotFoundError):
            get_options(argument_list)

    @pytest.mark.regression
    @pytest.mark.invalid
    @pytest.mark.negative
    def test_invalid_uri(self):
        # Arrange
        argument_list = ['script_name', '-d', 'invalid_database_uri']

        # Act and Assert
        with pytest.raises(sqlite3.OperationalError):
            get_options(argument_list)

