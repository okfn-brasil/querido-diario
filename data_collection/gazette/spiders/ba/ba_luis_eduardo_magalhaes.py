from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaLuisEduardoMagalhaesSpider(BaseDiofSpider):
    TERRITORY_ID = "2919553"
    name = "ba_luis_eduardo_magalhaes"
    website = "https://sai.io.org.br/ba/luiseduardomagalhaes/site/diariooficial"
    start_date = date(2017, 1, 4)
    power = "executive"
