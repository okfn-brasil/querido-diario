from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaAndorinhaSpider(BaseDiofSpider):
    TERRITORY_ID = "2901353"
    name = "ba_andorinha"
    website = "https://sai.io.org.br/ba/andorinha/site/diariooficial"
    start_date = date(2013, 1, 2)
    power = "executive"
