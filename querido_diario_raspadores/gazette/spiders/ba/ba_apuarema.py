from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaApuaremaSpider(BaseDiofSpider):
    TERRITORY_ID = "2901957"
    name = "ba_apuarema"
    website = "https://diario.apuarema.ba.gov.br"
    start_date = date(2009, 1, 23)
    power = "executive"
