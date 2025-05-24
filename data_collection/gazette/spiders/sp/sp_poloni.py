from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPoloniSpider(BaseInstarSpider):
    TERRITORY_ID = "3539905"
    name = "sp_poloni"
    base_url = "https://www.poloni.sp.gov.br/portal/diario-oficial"
    start_date = date(2022, 11, 4)
