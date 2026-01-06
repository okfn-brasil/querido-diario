from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaAramariSpider(BaseDiofSpider):
    TERRITORY_ID = "2902203"
    name = "ba_aramari"
    website = "https://diario.aramari.ba.gov.br"
    start_date = date(2009, 2, 12)
    power = "executive"
