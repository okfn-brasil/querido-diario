from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaNovaSoureSpider(BaseDiofSpider):
    TERRITORY_ID = "2922904"
    name = "ba_novasoure"
    website = "https://diario.novasoure.ba.gov.br/homepage"
    start_date = date(2008, 10, 7)
    power = "executive"
