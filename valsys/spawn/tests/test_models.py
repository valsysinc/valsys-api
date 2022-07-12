from dataclasses import dataclass
from valsys.spawn.models import FormulaEditConfig, MasterPopulateModulesConfig, PopulateModulesConfig, LineItemConfig, SpawnerProgress
import pytest


class TestFormulaEditConfig:
    def test_works_ok(self):
        period_name = 'pn'
        period_year = 'py'
        formula = 'form'
        fec = FormulaEditConfig(period_name=period_name, period_year=period_year, formula=formula)
        assert fec.formula == formula
        assert fec.period_name == period_name
        assert fec.period_year == period_year

    def test_from_json(self):
        period_name = 'pn'
        period_year = 'py'
        formula = 'form'
        input_json = {
            'periodName': period_name,
            'periodYear': period_year,
            'formula': formula
        }
        fec_fk = FormulaEditConfig.from_json(input_json)
        assert fec_fk.formula == formula
        assert fec_fk.period_name == period_name
        assert fec_fk.period_year == period_year

    def test_from_json_no_formula(self):
        period_name = 'pn'
        period_year = 'py'

        input_json = {
            'periodName': period_name,
            'periodYear': period_year,
        }
        with pytest.raises(ValueError) as err:
            FormulaEditConfig.from_json(input_json)
        assert 'formula' in str(err)

    def test_from_json_no_period_year(self):
        period_name = 'pn'
        formula = 'form'

        input_json = {
            'periodName': period_name,
            'formula': formula
        }
        with pytest.raises(ValueError) as err:
            FormulaEditConfig.from_json(input_json)
        assert 'periodYear' in str(err)

    def test_from_json_no_period_year_or_formula(self):
        period_name = 'pn'

        input_json = {
            'periodName': period_name,

        }
        with pytest.raises(ValueError) as err:
            FormulaEditConfig.from_json(input_json)
        assert 'periodYear' in str(err)
        assert 'formula' in str(err)


class TestPopulateModulesConfig:
    def test_min_input(self):
        tickers = ['t1', 't2']
        pmn = 'parent'
        mn = 'module'
        pmc = PopulateModulesConfig(tickers=tickers, parent_module_name=pmn, module_name=mn)
        assert pmc.tickers == tickers
        assert pmc.parent_module_name == pmn
        assert pmc.module_name == mn

    def test_bad_input(self):
        tickers = ['t1', 't2']
        pmn = 'parent'
        mn = 'module'
        with pytest.raises(ValueError) as err:
            PopulateModulesConfig(tickers=tickers, parent_module_name=pmn, module_name='')
        assert 'moduleName' in str(err)
        with pytest.raises(ValueError) as err:
            PopulateModulesConfig(tickers=tickers, parent_module_name='', module_name='mn')
        assert 'parentModuleName' in str(err)

    def test_set_model_ids(self):
        tickers = ['t1', 't2']
        pmn = 'parent'
        mn = 'module'
        pmc = PopulateModulesConfig(tickers=tickers, parent_module_name=pmn, module_name=mn)
        assert pmc.model_ids == []
        model_ids = [1, 2, 3]
        pmc.set_model_ids(model_ids)
        assert pmc.model_ids == model_ids

    def test_get_line_item_config(self):
        name1, name2 = 'n1', 'n2'
        o1, o2 = 1, 2
        lic1 = LineItemConfig(name=name1, order=o1)
        lic2 = LineItemConfig(name=name2, order=o2)
        tickers = ['t1', 't2']
        pmn = 'parent'
        mn = 'module'
        pmc = PopulateModulesConfig(tickers=tickers, parent_module_name=pmn,
                                    module_name=mn, line_item_data=[lic1, lic2])
        lic = pmc.get_line_item_config(line_item_name=name1)
        assert lic.name == name1
        assert lic.order == o1

    def test_get_line_item_config_not_found_with_line_items(self):
        name1, name2 = 'n1', 'n2'
        o1, o2 = 1, 2
        lic1 = LineItemConfig(name=name1, order=o1)
        lic2 = LineItemConfig(name=name2, order=o2)
        tickers = ['t1', 't2']
        pmn = 'parent'
        mn = 'module'
        pmc = PopulateModulesConfig(tickers=tickers, parent_module_name=pmn,
                                    module_name=mn, line_item_data=[lic1, lic2])
        with pytest.raises(ValueError) as err:
            pmc.get_line_item_config(line_item_name='name3')
        assert 'name3' in str(err)

    def test_get_line_item_config_not_found_with_no_line_items(self):
        tickers = ['t1', 't2']
        pmn = 'parent'
        mn = 'module'
        pmc = PopulateModulesConfig(tickers=tickers, parent_module_name=pmn,
                                    module_name=mn)
        with pytest.raises(ValueError) as err:
            pmc.get_line_item_config(line_item_name='name3')
        assert 'name3' in str(err)


class TestMasterPopulateModulesConfig:
    def test_works_no_input(self):
        mpmc = MasterPopulateModulesConfig()
        assert mpmc.modules_config == []

    def test_no_json(self):
        input_config = None
        mpmc = MasterPopulateModulesConfig.from_json(input_config)
        assert len(mpmc.modules_config) == 0

    def test_works_ok_from_json(self):
        input_config = [{'tickers': ['t1'], 'parentModuleName':'pmod1', 'moduleName':'mondname1'},
                        {'tickers': ['t2'], 'parentModuleName':'pmod2', 'moduleName':'mondname2'}]
        mpmc = MasterPopulateModulesConfig.from_json(input_config)
        assert len(mpmc.modules_config) == len(input_config)
        t = []
        for mc in mpmc:
            t.append(mc.tickers)
        assert t == [['t1'], ['t2']]


@dataclass
class FakeProcess:
    spawned: bool = False
    ticker: str = ''
    model_id: str = ''


class TestSpawnerProgress:
    def test_init(self):
        sp = SpawnerProgress()
        assert len(sp.processes) == 0

    def test_append(self):
        sp = SpawnerProgress()
        assert len(sp.processes) == 0
        sp.append(1)
        assert len(sp.processes) == 1
        sp.append(1.1)
        assert len(sp.processes) == 2

    def test_spawned_yes(self):
        sp = SpawnerProgress()
        sp.append(FakeProcess(spawned=True))
        sp.append(FakeProcess(spawned=False))
        assert sp.has_errors is False

    def test_spawned_tickers(self):
        sp = SpawnerProgress()
        sp.append(FakeProcess(spawned=True, ticker='t1'))
        sp.append(FakeProcess(spawned=True, ticker='t11'))
        sp.append(FakeProcess(spawned=False, ticker='t2'))
        sp.append(FakeProcess(spawned=False, ticker='t22'))
        assert sp.spawned_tickers == ['t1', 't11']

    def test_spawned_model_ids_for_tickers(self):
        sp = SpawnerProgress()
        sp.append(FakeProcess(spawned=True, ticker='t1', model_id='1'))
        sp.append(FakeProcess(spawned=True, ticker='t11', model_id='2'))
        sp.append(FakeProcess(spawned=False, ticker='t2', model_id='3'))
        sp.append(FakeProcess(spawned=False, ticker='t22', model_id='4'))
        assert sp.spawned_model_ids_for_tickers(['t1']) == ['1']
        assert sp.spawned_model_ids_for_tickers(['t1', 't11']) == ['1', '2']
        assert sp.spawned_model_ids_for_tickers(['t1', 't11', 't2']) == ['1', '2']
        assert sp.spawned_model_ids_for_tickers(['t1',  't2']) == ['1']
