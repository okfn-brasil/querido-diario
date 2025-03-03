from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaAracasSpider(BaseDiofSpider):
    TERRITORY_ID = "2902054"
    name = "ba_aracas"
    website = "https://diario.aracas.ba.gov.br"
    start_date = date(2014, 11, 27)
    power = "executive"
