from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaSantaLuziaSpider(BaseDiofSpider):
    TERRITORY_ID = "2928059"
    name = "ba_santa_luzia_2024"
    website = "https://diario.santaluzia.ba.gov.br"
    start_date = date(2024, 1, 5)
    power = "executive"
