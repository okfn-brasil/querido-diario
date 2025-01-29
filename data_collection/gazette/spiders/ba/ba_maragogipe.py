from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaMaragogipeSpider(BaseDiofSpider):
    TERRITORY_ID = "2920601"
    name = "ba_maragogipe"
    website = "https://sai.io.org.br/ba/maragojipe/site/diariooficial"
    start_date = date(2011, 2, 2)
    power = "executive"
