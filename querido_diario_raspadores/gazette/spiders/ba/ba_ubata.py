from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaUbataSpider(BaseDiofSpider):
    TERRITORY_ID = "2932309"
    name = "ba_ubata"
    website = "https://diario.ubata.ba.gov.br/homepage"
    start_date = date(2005, 5, 30)
    power = "executive"
