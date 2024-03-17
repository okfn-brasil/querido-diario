from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgJuatubaSpider(BaseInstarSpider):
    TERRITORY_ID = "3136652"
    name = "mg_juatuba"
    allowed_domains = ["juatuba.mg.gov.br"]
    base_url = "https://www.juatuba.mg.gov.br/portal/diario-oficial"
    start_date = date(2016, 1, 5)
