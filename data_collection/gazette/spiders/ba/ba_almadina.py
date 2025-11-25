from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaAlmadinaSpider(BaseDiofSpider):
    TERRITORY_ID = "2900900"
    name = "ba_almadina"
    website = "https://diario.almadina.ba.gov.br"
    start_date = date(2005, 1, 3)
    power = "executive"
