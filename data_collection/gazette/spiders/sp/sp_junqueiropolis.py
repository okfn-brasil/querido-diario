from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpJunqueiropolisSpider(BaseInstarSpider):
    TERRITORY_ID = "3526001"
    name = "sp_junqueiropolis"
    base_url = "https://www.junqueiropolis.sp.gov.br/portal/diario-oficial"
    start_date = date(2020, 10, 24)
