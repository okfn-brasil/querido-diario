from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgPiranguinhoSpider(BaseInstarSpider):
    TERRITORY_ID = "3151008"
    name = "mg_piranguinho"
    base_url = "https://www.piranguinho.mg.gov.br/portal/diario-oficial"
    start_date = date(2018, 7, 30)
