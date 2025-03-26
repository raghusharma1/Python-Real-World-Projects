import pytest
from hello_world import greeting

class Test_HelloWorldGreeting:

  def test_greeting_default_value(self, capsys):
    greeting()
    captured = capsys.readouterr()
    assert captured.out == 'Hello, World!\n'

  
  def test_greeting_custom_value(self, capsys):
    greeting('John')
    captured = capsys.readouterr()
    assert captured.out == 'Hello, John!\n'

  
  def test_greeting_exception_handling(self):
    with pytest.raises(TypeError):
      greeting(123)
