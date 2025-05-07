from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpAvanhandavaSpider(BaseInstarSpider):
    TERRITORY_ID = "3504404"
    name = "sp_avanhandava"
    base_url = "https://www.avanhandava.sp.gov.br/portal/diario-oficial"
    start_date = date(2022, 1, 7)
