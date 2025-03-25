import pytest
from fake_cli_steps import step_impl


class Test_FakeCliStepsStepImpl:
    @pytest.mark.regression
    def test_step_impl_success(self):
        # Arrange
        context = {'scenario': 'implemented'}

        # Act
        result = None
        try:
            step_impl(context)
        except Exception as e:
            result = e

        # Assert
        assert result is None, 'An exception or error was raised during function execution'

    @pytest.mark.regression
    def test_step_impl_unimplemented_scenario(self):
        # Arrange
        context = {'scenario': 'unimplemented'}
        expected_message = u'STEP: Then the log contains "File not found: Anscombe_quartet_data.csv"'

        # Act and Assert
        with pytest.raises(NotImplementedError) as excinfo:
            step_impl(context)
        assert str(excinfo.value) == expected_message, 'Unexpected exception message for unimplemented scenario'

    @pytest.mark.negative
    def test_step_impl_null_context(self):
        # Arrange
        context = None

        # Act and Assert
        with pytest.raises(TypeError):
            step_impl(context)
