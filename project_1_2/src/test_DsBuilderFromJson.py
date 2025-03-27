import pytest
from kaggle_client import DSBuilder
from model import Dataset  

class Test_DsBuilderFromJson:
    valid_json = {
        'title': 'dataset1',
        'ref': 'ref1',
        'url': 'www.url.com',
        'totalBytes': '1000',
        'viewCount': '100',
        'voteCount': '10',
        'downloadCount': '100',
        'usabilityRating': '5'
    }
    
    @pytest.mark.positive
    @pytest.mark.regression
    def test_from_json_with_correct_data(self):
        # Arrange
        ds_builder = DSBuilder(Dataset)
        
        # Act
        result = ds_builder.from_json(self.valid_json)

        # Assert
        assert isinstance(result, Dataset)
        assert result.title == self.valid_json['title']
        assert result.ref == self.valid_json['ref']
        assert result.url == self.valid_json['url']
        assert result.totalBytes == int(self.valid_json['totalBytes'])
        assert result.viewCount == int(self.valid_json['viewCount'])
        assert result.voteCount == int(self.valid_json['voteCount'])
        assert result.downloadCount == int(self.valid_json['downloadCount'])
        assert result.usabilityRating == int(self.valid_json['usabilityRating'])

    @pytest.mark.negative
    @pytest.mark.regression
    def test_from_json_with_partial_data(self):
        # Arrange
        invalid_json = { key: self.valid_json[key] for key in list(self.valid_json.keys())[:5] }
        ds_builder = DSBuilder(Dataset)

        # Act & Assert
        with pytest.raises(KeyError):
            result = ds_builder.from_json(invalid_json)

    @pytest.mark.negative
    @pytest.mark.regression
    def test_from_json_with_incorrect_datatypes(self):
        # Arrange
        invalid_json = self.valid_json.copy()
        invalid_json['totalBytes'] = 'one thousand'
        ds_builder = DSBuilder(Dataset)

        # Act & Assert
        with pytest.raises(ValueError):
            result = ds_builder.from_json(invalid_json)

    @pytest.mark.negative
    @pytest.mark.regression
    def test_from_json_with_non_pythonic_data(self):
        # Arrange
        invalid_json = self.valid_json.copy()
        invalid_json['totalBytes'] = float('NaN')
        ds_builder = DSBuilder(Dataset)

        # Act & Assert
        with pytest.raises((ValueError, TypeError)):  
            result = ds_builder.from_json(invalid_json)
