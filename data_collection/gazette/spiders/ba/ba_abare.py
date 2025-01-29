from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaAbareSpider(BaseDiofSpider):
    TERRITORY_ID = "2900207"
    name = "ba_abare"
    website = "https://sai.io.org.br/ba/abare/site/diariooficial"
    start_date = date(2007, 1, 9)
    power = "executive"
