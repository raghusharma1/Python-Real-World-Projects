import pytest
from unittest import mock
from unittest.mock import MagicMock
from environment import after_scenario
from collections.abc import Iterator
from typing import Any
import subprocess
import time
import os
import sys
from behave import fixture, use_fixture
from behave.runner import Context


class Test_EnvironmentAfterScenario:

    @pytest.mark.regression
    def test_temp_path_deletion(self):
        # Arrange
        context = Context()
        context.temp_path = MagicMock()
        scenario = mock.Mock()

        # Act
        after_scenario(context, scenario)

        # Assert
        context.temp_path.unlink.assert_called_once()

    @pytest.mark.regression
    def test_context_without_temp_path(self):
        # Arrange
        context = Context()
        scenario = mock.Mock()

        # Act
        try:
            after_scenario(context, scenario)
            error = None
        except Exception as e:
            error = e

        # Assert
        assert error is None

    @pytest.mark.regression
    def test_context_type(self):
        # Arrange
        contexts = [Context(), "context", 123, True, ["context"], {"context": ""}]

        for context in contexts:
            scenario = mock.Mock()

            # Act 
            try:
                after_scenario(context, scenario)
                error = None
            except Exception as e:
                error = e

            # Assert
            # Expecting exception when a wrong context type is given
            # As our function expects Context object, only in that case error should be None
            if isinstance(context, Context):
                assert error is None
            else:
                assert error is not None

    @pytest.mark.regression
    def test_scenario_type(self):
        # Arrange
        scenarios = ["scenario", 123, True, ["scenario"], {"scenario": ""}, mock.Mock()]

        for scenario in scenarios:
            context = Context()

            # Act 
            try:
                after_scenario(context, scenario)
                error = None
            except Exception as e:
                error = e

            # Assert
            # Expecting exception when a wrong scenario type is given
            # as our function operates correctly with mock scenarios
            if isinstance(scenario, mock.Mock):
                assert error is None
            else:
                assert error is not None
