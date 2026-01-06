from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaJaborandiSpider(BaseDiofSpider):
    TERRITORY_ID = "2917359"
    name = "ba_jaborandi"
    website = "https://sai.io.org.br/ba/jaborandi/site/diariooficial"
    start_date = date(2022, 3, 4)
    power = "executive"
