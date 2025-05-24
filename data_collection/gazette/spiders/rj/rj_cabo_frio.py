from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class RjCaboFrioSpider(BaseInstarSpider):
    name = "rj_cabo_frio"
    TERRITORY_ID = "3300704"
    base_url = "https://www.cabofrio.instartecnologia.com.br/portal/diario-oficial"
    start_date = date(2020, 7, 29)
    power = "executive"
