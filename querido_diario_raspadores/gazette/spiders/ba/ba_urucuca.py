from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaUrucucaSpider(BaseDiofSpider):
    TERRITORY_ID = "2932705"
    name = "ba_urucuca"
    website = "https://sai.io.org.br/ba/urucuca/Site/DiarioOficial"
    start_date = date(2005, 8, 18)
    power = "executive"
