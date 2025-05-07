from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpItapolisSpider(BaseInstarSpider):
    TERRITORY_ID = "3522703"
    name = "sp_itapolis"
    base_url = "https://www.itapolis.sp.gov.br/portal/diario-oficial"
    start_date = date(2017, 1, 11)
