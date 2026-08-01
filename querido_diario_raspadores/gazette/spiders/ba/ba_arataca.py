from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaAratacaSpider(BaseDiofSpider):
    TERRITORY_ID = "2902252"
    name = "ba_arataca"
    website = "https://diario.arataca.ba.gov.br"
    start_date = date(2005, 1, 13)
    power = "executive"
