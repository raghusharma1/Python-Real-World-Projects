import pytest
import hw

class Test_HwGreeting:
    
    # Test Scenario 1: Default greeting value
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_greeting_default_value(self, capsys):
        hw.greeting()
        captured = capsys.readouterr()
        assert captured.out == 'Hello, World!\n'
    
    # Test Scenario 2: Custom greeting
    @pytest.mark.regression
    def test_greeting_custom_value(self, capsys):
        hw.greeting("Python")
        captured = capsys.readouterr()
        assert captured.out == 'Hello, Python!\n'
    
    # Test Scenario 3: Exception handling
    @pytest.mark.negative
    def test_greeting_exception_handling(self, capsys):
        with pytest.raises(TypeError):
            hw.greeting(123)
