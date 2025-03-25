import pytest
from kaggle_client import find_json
from bs4 import BeautifulSoup
from pathlib import Path
from unittest.mock import patch
import json
from model import DS

@pytest.mark.valid
def test_json_data_parsing(monkeypatch):
    test_data = {"username": "test_user", "key": "test_key"}

    monkeypatch.setattr(Path, "home", lambda: Path("."))
    with open("Downloads/kaggle.json", "w") as f:
        f.write(json.dumps(test_data))

    def mock_open(*args, **kwargs):
        return json.dumps(test_data)

    with patch("builtins.open", mock_open):
        find_json()

    assert test_data["username"] == "test_user" 
    assert test_data["key"] == "test_key"

@pytest.mark.valid
def test_rest_access_reader_functioning(monkeypatch):
    reader_content = "Reader Content"
    
    def mock_get_paged_json(*args, **kwargs):
        return iter([reader_content])

    monkeypatch.setattr("kaggle_client.RestAccess.get_paged_json", mock_get_paged_json)

    assert find_json() == reader_content

@pytest.mark.valid
def test_dataset_builder(monkeypatch):
    fake_row = { "id": "test_id", "name": "test_name", "licenseName" : "test_license", 
                 "ownerName": "test_owner", "size": "test_size", 
                 "usabilityRating": "test_usability" }

    def mock_from_json(*args, **kwargs):
        fake_ds = DS(*list(fake_row.values()))
        return fake_ds

    monkeypatch.setattr("kaggle_client.DSBuilder.from_json", mock_from_json)

    ds = find_json()
    
    assert ds.id == "test_id"
    assert ds.name == "test_name"
    assert ds.licenseName == "test_license"
    assert ds.size == "test_size"
    assert ds.usabilityRating == "test_usability"

@pytest.mark.valid
def test_usability_rating_filter(monkeypatch):
    fake_rows = [ { "id": "test_id" + str(i), "name": "test_name" + str(i), 
                   "ownerName": "test_owner" + str(i), 
                   "size": "test_size" + str(i), 
                   "usabilityRating": i/10 } for i in range(10) ]

    def mock_get_paged_json(*args, **kwargs):
        return iter(fake_rows)

    monkeypatch.setattr("kaggle_client.RestAccess.get_paged_json", mock_get_paged_json)
    
    filtered_ds = find_json()

    for ds in filtered_ds:
        assert ds.usabilityRating > 0.5
