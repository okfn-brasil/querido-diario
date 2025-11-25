from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpIracemapolisSpider(BaseInstarSpider):
    TERRITORY_ID = "3521408"
    name = "sp_iracemapolis"
    base_url = "https://www.iracemapolis.sp.gov.br/portal/diario-oficial"
    start_date = date(2017, 1, 2)
