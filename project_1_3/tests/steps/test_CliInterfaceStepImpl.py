import pytest
from unittest.mock import Mock
from cli_interface import step_impl

class Test_CliInterfaceStepImpl:

    @pytest.mark.regression
    @pytest.mark.positive
    def test_log_line_in_output(self):
        mock_context = Mock()
        mock_context.output = "Sample log line"

        log_line = "Sample log line"

        # Act
        step_impl(mock_context, log_line)

        # Assert
        mock_context.output.assert_called()
        

    @pytest.mark.regression
    @pytest.mark.negative
    def test_log_line_not_in_output(self):
        mock_context = Mock()
        mock_context.output = "Another log line"

        log_line = "Sample log line"

        # Act and Assert
        with pytest.raises(AssertionError) as e_info:
            step_impl(mock_context, log_line)

        assert str(e_info.value) == f"No {log_line!r} in output"

    @pytest.mark.regression
    @pytest.mark.negative
    def test_empty_context_output(self):
        mock_context = Mock()
        mock_context.output = ""

        log_line = "Sample log line"

        # Act and Assert
        with pytest.raises(AssertionError) as e_info:
            step_impl(mock_context, log_line)

        assert str(e_info.value) == f"No {log_line!r} in output"
