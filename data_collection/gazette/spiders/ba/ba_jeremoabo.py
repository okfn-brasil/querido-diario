from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaJeremoaboSpider(BaseDiofSpider):
    TERRITORY_ID = "2918100"
    name = "ba_jeremoabo"
    website = "https://diario.jeremoabo.ba.gov.br"
    start_date = date(2010, 7, 8)
    power = "executive"
