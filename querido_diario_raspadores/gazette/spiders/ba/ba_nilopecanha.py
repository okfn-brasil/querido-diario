from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaNiloPecanhaSpider(BaseDiofSpider):
    TERRITORY_ID = "2922607"
    name = "ba_nilopecanha"
    website = "https://diario.nilopecanha.ba.gov.br/homepage"
    start_date = date(2007, 1, 15)
    power = "executive"
