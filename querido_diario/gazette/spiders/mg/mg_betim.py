from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgBetimSpider(BaseInstarSpider):
    TERRITORY_ID = "3106705"
    name = "mg_betim"
    base_url = "https://www.betim.mg.gov.br/portal/diario-oficial"
    start_date = date(2008, 1, 11)
