import csv
import io
import zipfile
from bottle import HTTPResponse, request
from mock_kaggle_bottle import datasets_download
import pytest


class Test_MockKaggleBottleDatasetsDownload:

    @pytest.mark.positive
    def test_successful_data_download(self):
        ownerSlug = "carlmcbrideellis"
        datasetSlug = "data-anscombes-quartet"
        response = datasets_download(ownerSlug, datasetSlug)

        # Assert Values
        assert response.status == 200
        assert "zip" in response.headers["Content-Type"]

    @pytest.mark.negative
    def test_non_existant_data(self):
        ownerSlug = "non-existing-owner"
        datasetSlug = "non-existing-data"
        response = datasets_download(ownerSlug, datasetSlug)

        # Assert Values
        assert response.status == 404

    @pytest.mark.positive
    def test_correct_data_in_response(self):
        ownerSlug = "carlmcbrideellis"
        datasetSlug = "data-anscombes-quartet"
        response = datasets_download(ownerSlug, datasetSlug)

        # Create expected CSV data as a zip file
        expected_zip_content = io.BytesIO()
        with zipfile.ZipFile(expected_zip_content, 'w') as archive:
            target_path = zipfile.Path(archive, 'Anscombe_quartet_data.csv')
            with target_path.open('w') as member_file:
                writer = csv.writer(member_file)
                writer.writerow(['mock', 'data'])
                writer.writerow(['line', 'two'])

        # Assert Values
        assert response.status == 200
        assert response.body == expected_zip_content.getvalue()

