import pytest
from sql_script_maker import write_insert


@pytest.mark.regression
@pytest.mark.valid
def test_insert_statement_with_valid_data():
    # Arrange
    series = 1
    sequence = 2
    x = 'A'
    y = 'B'
    expected_output = f"INSERT INTO SSAMPLES(SERIES, SEQUENCE, X, Y)VALUES({series}, {sequence}, '{x}', '{y}')"

    # Act
    result = write_insert(series, sequence, x, y)

    # Assert
    assert result == expected_output


@pytest.mark.regression
@pytest.mark.valid
def test_insert_statement_with_empty_strings():
    # Arrange
    series = 1
    sequence = 2
    x = ''
    y = ''
    expected_output = f"INSERT INTO SSAMPLES(SERIES, SEQUENCE, X, Y)VALUES({series}, {sequence}, '{x}', '{y}')"

    # Act
    result = write_insert(series, sequence, x, y)

    # Assert
    assert result == expected_output


@pytest.mark.regression
@pytest.mark.valid
def test_insert_statement_with_large_strings():
    # Arrange
    series = 1
    sequence = 2
    x = 'A'*500
    y = 'B'*500
    expected_output = f"INSERT INTO SSAMPLES(SERIES, SEQUENCE, X, Y)VALUES({series}, {sequence}, '{x}', '{y}')"

    # Act
    result = write_insert(series, sequence, x, y)

    # Assert
    assert result == expected_output


@pytest.mark.regression
@pytest.mark.valid
def test_insert_statement_with_special_chars():
    # Arrange
    series = 1
    sequence = 2
    x = "'); DROP TABLE USERS;"
    y = "'); ROLLBACK;"
    expected_output = f"INSERT INTO SSAMPLES(SERIES, SEQUENCE, X, Y)VALUES({series}, {sequence}, '{x}', '{y}')"

    # Act
    result = write_insert(series, sequence, x, y)

    # Assert
    assert result == expected_output
