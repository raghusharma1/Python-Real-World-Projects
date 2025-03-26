import pytest
from unittest.mock import Mock, sentinel, call
from csv_extract import Series1Pair

class DerivedRawData(RawData):
    pass

class Test_CsvExtractTestSeries1Pair:
    
    @pytest.mark.regression
    def test_mock_value_calls(self):
        mock_raw_class = Mock()
        p1 = Series1Pair()
        p1.target_class = mock_raw_class
        xypair = p1.from_row([sentinel.X, sentinel.Y])

        assert mock_raw_class.mock_calls == [
            call(sentinel.X, sentinel.Y)
        ], "Mock raw class did not receive correct calls from function test_series1pair."
        
    @pytest.mark.positive
    def test_derivative_raw_data_handling(self):
        p1 = Series1Pair()
        p1.target_class = DerivedRawData
        mock_row = ['10', '20']

        xypair = p1.from_row(mock_row)

        assert isinstance(xypair, XYPair)
        assert xypair.x == int(mock_row[0]) 
        assert xypair.y == int(mock_row[1]) 

    @pytest.mark.negative
    def test_unexpected_input_handling(self):
        p1 = Series1Pair()
        p1.target_class = DerivedRawData
        mock_row = ['10']

        try:
            xypair = p1.from_row(mock_row)
            assert True, "Function successfully handled unexpected input."
        except:
            assert False, "Function did not handle unexpected input successfully."
    
    @pytest.mark.valid
    def test_string_csv_input_handling(self):
        p1 = Series1Pair()
        p1.target_class = DerivedRawData
        csv_string = "10,20"

        xypair = p1.from_row(csv_string.split(','))

        assert isinstance(xypair, XYPair)
        assert xypair.x == 10 
        assert xypair.y == 20 
