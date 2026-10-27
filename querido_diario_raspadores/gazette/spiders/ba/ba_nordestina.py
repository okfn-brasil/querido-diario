from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaNordestinaSpider(BaseDiofSpider):
    TERRITORY_ID = "2922656"
    name = "ba_nordestina"
    website = "https://diario.nordestina.ba.gov.br/homepage"
    start_date = date(2009, 1, 21)
    power = "executive"
