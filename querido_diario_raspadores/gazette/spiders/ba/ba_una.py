from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaUnaSpider(BaseDiofSpider):
    TERRITORY_ID = "2932507"
    name = "ba_una"
    website = "https://diario.una.ba.gov.br/homepage"
    start_date = date(2006, 2, 3)
    power = "executive"
