from valsys.seeds.loader import SeedsLoader
from unittest import mock

MODULE_PREFIX = "valsys.seeds.loader"


class TestSeedsLoader:
    @mock.patch(f"{MODULE_PREFIX}.load_company_configs")
    def test_company_configs_no_tickers(self, mock_load_company_configs):
        loader = SeedsLoader()
        assert loader.company_configs_by_ticker([]) == []
        mock_load_company_configs.assert_not_called()

    @mock.patch(f"{MODULE_PREFIX}.load_company_configs")
    def test_company_configs_no_returned_tickers(self, mock_load_company_configs):
        mock_load_company_configs.return_value = []
        tickers = ['t1', 't2']
        loader = SeedsLoader()
        assert loader.company_configs_by_ticker(tickers) == []
        mock_load_company_configs.assert_called_once()

    @mock.patch(f"{MODULE_PREFIX}.load_company_configs")
    def test_company_configs_no_matching_tickers(self, mock_load_company_configs):
        mock_load_company_configs.return_value = [{'ticker': 't3'}, {'ticker': 't4'}]
        tickers = ['t1', 't2']
        loader = SeedsLoader()
        assert loader.company_configs_by_ticker(tickers) == []
        mock_load_company_configs.assert_called_once()

    @mock.patch(f"{MODULE_PREFIX}.load_company_configs")
    def test_company_configs_matching_tickers(self, mock_load_company_configs):
        mock_load_company_configs.return_value = [
            {'ticker': 't1', 'companyName': 'c1', 'industry': 'i1', 'startYears': [2, 1]},
            {'ticker': 't2', 'companyName': 'c2', 'industry': 'i2', 'startYears': [4, 3]}]
        tickers = ['t1', 't2']
        loader = SeedsLoader()
        company_configs = loader.company_configs_by_ticker(tickers)
        mock_load_company_configs.assert_called_once()
        assert len(company_configs) == 2
        tickers_found = [cc.ticker for cc in company_configs]
        assert set(tickers) == set(tickers_found)
