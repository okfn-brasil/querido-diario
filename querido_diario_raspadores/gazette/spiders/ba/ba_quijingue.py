from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaQuijingueSpider(BaseDiofSpider):
    TERRITORY_ID = "2925907"
    name = "ba_quijingue"
    website = "https://diario.quijingue.ba.gov.br/homepage"
    start_date = date(2007, 8, 15)
    power = "executive"
