from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaLauroDeFreitasSpider(BaseDiofSpider):
    TERRITORY_ID = "2919207"
    name = "ba_lauro_de_freitas"
    website = "https://sai.io.org.br/ba/laurodefreitas/site/diariooficial"
    start_date = date(2013, 7, 31)
    power = "executive"
