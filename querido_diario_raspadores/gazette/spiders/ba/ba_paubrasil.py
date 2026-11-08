from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaPauBrasilSpider(BaseDiofSpider):
    TERRITORY_ID = "2923902"
    name = "ba_paubrasil"
    website = "https://diario.paubrasil.ba.gov.br/homepage"
    start_date = date(2007, 3, 8)
    power = "executive"
