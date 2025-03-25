import pytest
import sqlite3
from pathlib import Path
import csv
from typing import Any
from dataclasses import dataclass, asdict
from contextlib import contextmanager
from build_db import main

@contextmanager
def does_not_raise():
    yield

class Test_BuildDbMain:

    @pytest.mark.parametrize("config_path, data_path, expectation", [
        # Scenario 1: Validate main function with correct config file and data file paths
        (Path.cwd() / "schema.toml", Path.cwd().parent / "data" / "Anscombe_quartet_data.csv", does_not_raise()),
        # Scenario 2: Validate main function with invalid config file
        (Path.cwd() / "invalid.toml", Path.cwd().parent / "data" / "Anscombe_quartet_data.csv", pytest.raises(Exception)),
        # Scenario 4: Validate main function with no data file or empty
        (Path.cwd() / "schema.toml", Path.cwd().parent / "data" / "empty.csv", pytest.raises(Exception))
       ])
    def test_main_function(self, config_path, data_path, expectation):
        with expectation:
            with sqlite3.connect("file:example.db", uri=True) as connection:
                main()
                

    # Scenario 3: Validate main function with no database
    def test_main_function_with_no_database(self):
        # Assuming schema.toml and Anscombe_quartet_data.csv are present in their respective locations.
        # Ensuring no 'example.db' file
        if Path('file:example.db').exists():
            Path('file:example.db').unlink()

        # invoke main function
        main()

        # Assert if 'example.db' created
        assert Path('file:example.db').exists(), "Database file 'example.db' not found."
