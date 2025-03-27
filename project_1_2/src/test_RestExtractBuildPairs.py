import pytest
from kaggle_client import RestExtract, PairBuilder, RawData

class Test_RestExtractBuildPairs:
    
    class StubPairBuilder(PairBuilder):
        def from_row(self, row: list[str]) -> RawData:
            return RawData('stub', row[0], row[0])
        
    @pytest.mark.regression
    def test_build_pairs_no_builders(self):
        rest_extract = RestExtract([])
        pairs = rest_extract.build_pairs(['sample'])
        assert pairs == []

    @pytest.mark.regression
    def test_build_pairs_single_builder_single_row(self):
        rest_extract = RestExtract([self.StubPairBuilder()])
        pairs = rest_extract.build_pairs(['sample'])
        assert pairs == [RawData('stub', 'sample', 'sample')]

    @pytest.mark.regression
    def test_build_pairs_multiple_builders_multiple_rows(self):
        rest_extract = RestExtract([self.StubPairBuilder(), self.StubPairBuilder()])
        pairs = rest_extract.build_pairs(['sample1', 'sample2'])
        assert pairs == [RawData('stub', 'sample1', 'sample1'), RawData('stub', 'sample2', 'sample2')]

    @pytest.mark.regression
    def test_build_pairs_builders_no_rows(self):
        rest_extract = RestExtract([self.StubPairBuilder()])
        pairs = rest_extract.build_pairs([])
        assert pairs == []
