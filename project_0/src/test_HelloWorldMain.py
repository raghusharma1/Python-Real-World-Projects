import pytest
import argparse
import sys
from hello_world import main
from unittest import mock

class Test_HelloWorldMain:

    @mock.patch('hello_world.greeting')
    @mock.patch('hello_world.get_options')
    @pytest.mark.parametrize("args", [(["--who", "Tester"])])
    def test_main_with_valid_args(self, mock_get_options, mock_greeting, args):
        main(args)
        mock_get_options.assert_called_once_with(args)
        mock_greeting.assert_called_once()

    @mock.patch('hello_world.get_options')
    def test_main_without_args(self, mock_get_options):
        with pytest.raises((Exception, SystemExit)):
            main([])
        mock_get_options.assert_called_once_with([])

    @mock.patch('hello_world.get_options')
    @pytest.mark.parametrize("args", [("Incorrect",)])
    def test_main_with_inappropriate_arg_type(self, mock_get_options, args):
        with pytest.raises(TypeError):
            main(args)
        mock_get_options.assert_not_called()

    @mock.patch('hello_world.greeting')
    @mock.patch('hello_world.get_options')
    @pytest.mark.parametrize("args", [(["--foo", "bar"])])
    def test_main_with_erroneous_args(self, mock_get_options, mock_greeting, args):
        with pytest.raises((Exception, SystemExit)):
            main(args)
        mock_get_options.assert_called_once_with(args)
        mock_greeting.assert_not_called()
