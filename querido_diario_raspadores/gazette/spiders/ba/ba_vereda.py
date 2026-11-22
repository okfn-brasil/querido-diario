from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaVeredaSpider(BaseDiofSpider):
    TERRITORY_ID = "2933257"
    name = "ba_vereda"
    website = "https://sai.io.org.br/ba/vereda/Site/DiarioOficial"
    start_date = date(2010, 12, 30)
    power = "executive"
