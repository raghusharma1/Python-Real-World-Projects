import argparse
import pytest
import sys
from hello_world import get_options


@pytest.mark.positive
def test_default_parameter_handling():
    """Test default parameter handling."""
    # Arrange
    argv = []

    # Act
    result = get_options(argv)

    # Assert
    assert result.who == "World"


@pytest.mark.positive
def test_custom_input_handling():
    """Test custom input handling."""
    # Arrange
    custom_string = "Custom"
    argv = ["--who", custom_string]

    # Act
    result = get_options(argv)

    # Assert
    assert result.who == custom_string


@pytest.mark.positive
def test_multiple_parameter_handling():
    """Test multiple parameter handling."""
    # Arrange
    custom_string1 = "Custom1"
    custom_string2 = "Custom2"
    argv = ["--who", custom_string1, "--who", custom_string2]

    # Act
    result = get_options(argv)

    # Assert
    assert result.who == custom_string2


@pytest.mark.positive
def test_short_notation_handling():
    """Test short notation handling."""
    # Arrange
    custom_string = "Custom"
    argv = ["-w", custom_string]

    # Act
    result = get_options(argv)

    # Assert
    assert result.who == custom_string


if __name__ == "__main__":
    pytest.main([__file__])
