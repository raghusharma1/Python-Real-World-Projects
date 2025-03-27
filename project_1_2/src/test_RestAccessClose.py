import pytest
from kaggle_client import RestAccess
import requests

class Test_RestAccessClose:

    @pytest.mark.smoke
    def test_close_on_initialized_object(self):
        # Arrange
        credentials = {
            "username": "test_username",
            "key": "test_key"
        }
        client = RestAccess(credentials)

        # Act and Assert
        try:
            client.close()
            assert True
        except:
            assert False, "Exception occurred while closing the client."

    @pytest.mark.regression
    def test_multiple_calls_to_close(self):
        # Arrange
        credentials = {
            "username": "test_username",
            "key": "test_key"
        }
        client = RestAccess(credentials)

        # Act and Assert
        try:
            for _ in range(5):
                client.close()
            assert True
        except:
            assert False, "Exception occurred while closing the client multiple times."

    @pytest.mark.negative
    def test_close_without_initialization(self):
        # Arrange
        client = RestAccess({
            "username": "",
            "key": ""
        })

        # Act and Assert
        with pytest.raises(requests.exceptions.InvalidHeader):
            client.close()

    @pytest.mark.regression
    def test_close_after_operation(self):
        # Arrange
        credentials = {
            "username": "test_username",
            "key": "test_key"
        }
        client = RestAccess(credentials)

        # Suppose perform_operation changes the state of client
        client.perform_operation()

        # Act and Assert
        try:
            client.close()
            assert True
        except:
            assert False, "Exception occurred while closing the client after an operation."
