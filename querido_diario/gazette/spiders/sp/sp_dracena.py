from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpDracenaSpider(BaseInstarSpider):
    TERRITORY_ID = "3514403"
    name = "sp_dracena"
    base_url = "https://www.dracena.sp.gov.br/portal/diario-oficial"
    start_date = date(2020, 11, 24)
