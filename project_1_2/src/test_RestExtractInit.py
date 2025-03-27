import pytest
import requests
from kaggle_client import RestExtract, PairBuilder


class Test_RestExtractInit:
    # Test Scenario 1: Validating correct initialization of kaggle_doc based constructor
    def test_kaggle_doc_initialization(self):
        kaggle_doc = {"username": "test_user", "key": "test_key"}    # Test Kaggle Doc
        rest_extract = RestExtract(kaggle_doc)
        assert isinstance(rest_extract.credentials, requests.auth.HTTPBasicAuth)    # Check if the object is of type HTTPBasicAuth

    # Test Scenario 2: Validating correct initialization of builders based constructor
    def test_builders_initialization(self):
        builders = [PairBuilder("PairBuilder1"), PairBuilder("PairBuilder2")]    # Test PairBuilders
        rest_extract = RestExtract(builders)
        assert isinstance(rest_extract.builders, list) and all(isinstance(builder, PairBuilder) for builder in rest_extract.builders), "All builders are not of type PairBuilder"

    # Test Scenario 3: Validating builders input as empty list
    def test_empty_builders_initialization(self):
        builders = []    # Empty list of PairBuilders
        rest_extract = RestExtract(builders)
        assert rest_extract.builders == [], "Builders are not initialized as empty list"

    # Test Scenario 4: Validating kaggle_doc input as empty dictionary
    def test_empty_kaggle_doc_initialization(self):
        kaggle_doc = {}    # Empty Kaggle Doc
        with pytest.raises(KeyError):    # KeyError is expected as 'username' and 'key' keys are absent
            rest_extract = RestExtract(kaggle_doc)
