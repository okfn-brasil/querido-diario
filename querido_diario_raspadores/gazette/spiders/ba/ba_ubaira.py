from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaUbairaSpider(BaseDiofSpider):
    TERRITORY_ID = "2932101"
    name = "ba_ubaira"
    website = "https://diario.ubaira.ba.gov.br/homepage"
    start_date = date(2006, 11, 17)
    power = "executive"
