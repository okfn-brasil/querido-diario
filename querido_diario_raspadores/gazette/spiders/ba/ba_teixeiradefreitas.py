from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaTeixeiraDeFreitasSpider(BaseDiofSpider):
    TERRITORY_ID = "2931350"
    name = "ba_teixeiradefreitas"
    website = "https://sai.io.org.br/ba/teixeiradefreitas/Site/DiarioOficial"
    start_date = date(2007, 9, 11)
    power = "executive"
