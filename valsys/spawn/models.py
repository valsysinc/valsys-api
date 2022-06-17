import datetime


class ModelConfiguration:
    @classmethod
    def from_row(cls, row, proj_period, hist_period, period_type='ANNUAL', cash_flow_type='FCFF', valuation_type='Perpetual Growth', company_type='Public', target_variable='Implied share price'):
        return {
            "companyName": row.companyName,
            "ticker": row.ticker,
            "templateID": row.template_id,
            "projectionPeriod": proj_period,  # 11 kurt suggested, confirmed by valsys
            "historicalPeriod": hist_period,  # same as above
            "industry": row.IndustryGroup,
            "startPeriod":  row.fiscalYear,
            "startDate": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "type": "DEFAULT",
            "periodType": period_type,
            "cashFlowType": cash_flow_type,
            "valuationType": valuation_type,
            "companyType": company_type,
            "targetVariable": target_variable,
            "variables": {"INTERNAL_SOURCE": row.source},
            "historicalMax": row.fiscalYear - hist_period + 1,
            "historicalMin": row.fiscalYear + proj_period
        }
