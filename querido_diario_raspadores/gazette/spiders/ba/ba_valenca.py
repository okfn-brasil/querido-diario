from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaValencaSpider(BaseDiofSpider):
    TERRITORY_ID = "2933158"
    name = "ba_valenca"
    website = "https://diario.valenca.ba.gov.br/homepage"
    start_date = date(2009, 1, 2)
    power = "executive"
