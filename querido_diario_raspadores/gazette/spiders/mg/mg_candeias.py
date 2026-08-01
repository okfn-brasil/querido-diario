from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgCandeiasSpider(BaseInstarSpider):
    TERRITORY_ID = "3112000"
    name = "mg_candeias"
    base_url = "https://www.candeias.mg.gov.br/portal/diario-oficial"
    start_date = date(2017, 2, 8)
