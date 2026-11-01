from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaUbaitabaSpider(BaseDiofSpider):
    TERRITORY_ID = "2932200"
    name = "ba_ubaitaba"
    website = "https://diario.ubaitaba.ba.gov.br/homepage"
    start_date = date(2007, 6, 29)
    power = "executive"
