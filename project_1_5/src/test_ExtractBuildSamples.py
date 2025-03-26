import pytest
import model
import sqlite3
from typing import Any
from collections.abc import Iterator
from db_extract import build_samples

class Test_ExtractBuildSamples:

    # Scenario 1: Validating Successful Sample Retrieval.
    @pytest.mark.succesful_retrieval
    def test_successful_sample_retrieval(self):
        # Arrange
        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE Samples(x real, y real)")
        cursor.execute("INSERT INTO Samples VALUES(1.0, 2.0)")
        config = {
            'query': {
                'samples': "SELECT * FROM Samples WHERE name=:name",
            },
            'samples': 'Samples'
        }
        # Act
        samples = build_samples(connection, config, 'Samples')
        # Assert
        assert len(samples) > 0
        assert samples[0].x == 1.0
        assert samples[0].y == 2.0

    # Scenario 2: Error Handling when Config Dictionary Lacks Expected 'query' and/or 'samples' Keys.
    @pytest.mark.error_handling
    def test_missing_query_or_samples_keys(self):
        # Arrange
        connection = sqlite3.connect(':memory:')
        config_without_query = { 'samples': 'Samples' }
        config_without_samples = { 'query': { 'samples': "SELECT * FROM Samples WHERE name=:name" } }
        # Act & Assert
        with pytest.raises(KeyError):
            build_samples(connection, config_without_query, 'Samples')
        with pytest.raises(KeyError):
            build_samples(connection, config_without_samples, 'Samples')

    # Scenario 3: Testing Function’s Behaviour with Empty Database.
    @pytest.mark.empty_database
    def test_empty_database(self):
        # Arrange
        connection = sqlite3.connect(':memory:')
        config = {
            'query': {
                'samples': "SELECT * FROM Samples WHERE name=:name",
            },
            'samples': 'Samples'
        }
        # Act
        samples = build_samples(connection, config, 'Samples')
        # Assert
        assert len(samples) == 0
