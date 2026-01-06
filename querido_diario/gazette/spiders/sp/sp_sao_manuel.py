from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpSaoManuelSpider(BaseInstarSpider):
    TERRITORY_ID = "3550100"
    name = "sp_sao_manuel"
    base_url = "http://www.saomanuel.sp.gov.br/portal/diario-oficial"
    start_date = date(2016, 6, 7)
