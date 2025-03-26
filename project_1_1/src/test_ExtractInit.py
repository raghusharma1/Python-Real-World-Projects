# Start of Python Pytest

import pytest
from unittest.mock import Mock
from csv_extract import __init__ as init

class Test_ExtractInit:

    @pytest.mark.regression
    def test_init_correctly_sets_builders(self):
        # Arrange
        mock_builders = [Mock(), Mock(), Mock()]

        # Act
        extract = init.Extract(mock_builders)

        # Assert
        assert extract.builders == mock_builders, "Builders are not correctly initialized."

    @pytest.mark.smoke
    def test_builders_parameter_is_mutable(self):
        # Arrange
        mock_builders = [Mock(), Mock(), Mock()]
        extract = init.Extract(mock_builders)

        # Act
        new_mock_builder = Mock()
        extract.builders.append(new_mock_builder)

        # Assert
        assert extract.builders[-1] == new_mock_builder, "Builders are not mutable."

    @pytest.mark.negative
    def test_builders_parameter_not_none(self):
        # Arrange is not needed for this test.

        # Act and Assert
        with pytest.raises(TypeError, match="None is not allowed for builders."):
            _ = init.Extract(None)

    @pytest.mark.positive
    def test_empty_builders_list(self):
        # Arrange
        empty_builders = []

        # Act
        extract = init.Extract(empty_builders)
    
        # Assert
        assert extract.builders == empty_builders, "Builders list can not be empty."

# End of Python Pytest
