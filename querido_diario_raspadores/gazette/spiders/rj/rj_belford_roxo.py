from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class RjBelfordRoxoSpider(BaseInstarSpider):
    TERRITORY_ID = "3300456"
    name = "rj_belford_roxo"
    start_date = date(2019, 1, 2)
    power = "executive"
    base_url = "https://www.belfordr.instartecnologia.com.br/portal/diario-oficial"
