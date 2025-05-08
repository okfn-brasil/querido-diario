from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgJanuariaSpider(BaseInstarSpider):
    TERRITORY_ID = "3135209"
    name = "mg_januaria"
    base_url = "https://www.januaria.mg.gov.br/portal/diario-oficial"
    start_date = date(2022, 4, 29)
