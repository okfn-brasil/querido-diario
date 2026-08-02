from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaAdustinaSpider(BaseDiofSpider):
    TERRITORY_ID = "2900355"
    name = "ba_adustina"
    website = "https://diario.adustina.ba.gov.br"
    start_date = date(2017, 1, 3)
    power = "executive"
