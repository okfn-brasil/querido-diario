from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaAnageSpider(BaseDiofSpider):
    TERRITORY_ID = "2901205"
    name = "ba_anage"
    website = "https://diario.anage.ba.gov.br"
    start_date = date(2007, 1, 12)
    power = "executive"
