from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaMaragogipeSpider(BaseDiofSpider):
    TERRITORY_ID = "2916856"
    name = "ba_itatim"
    website = "https://diario.itatim.ba.gov.br"
    start_date = date(2009, 1, 1)
    power = "executive"
