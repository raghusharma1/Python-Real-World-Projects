import pytest
from hw import greeting
import sys
import io

class Test_HwGreeting:
    # Scenario 1: Check the default greeting
    def test_default_greeting(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            greeting()
            output = out.getvalue().strip()
            assert output == "Hello, World!"
        finally:
            sys.stdout = saved_stdout

    # Scenario 2: Greeting specified user
    def test_specified_greeting(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            greeting("Jane")
            output = out.getvalue().strip()
            assert output == "Hello, Jane!"
        finally:
            sys.stdout = saved_stdout

    # Scenario 3: Verify the greeting with special characters input
    def test_greeting_special_characters(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            greeting("@$#%")
            output = out.getvalue().strip()
            assert output == "Hello, @$#%!"
        finally:
            sys.stdout = saved_stdout

    # Scenario 4: Greeting empty user
    def test_empty_user_greeting(self):
        saved_stdout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            greeting("")
            output = out.getvalue().strip()
            assert output == "Hello, !"
        finally:
            sys.stdout = saved_stdout
