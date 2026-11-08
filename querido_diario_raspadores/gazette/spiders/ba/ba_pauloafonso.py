from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaPauloAfonsoSpider(BaseDiofSpider):
    TERRITORY_ID = "2924009"
    name = "ba_pauloafonso"
    website = "https://sai.io.org.br/ba/pauloafonso/Site/DiarioOficial"
    start_date = date(2009, 10, 26)
    power = "executive"
