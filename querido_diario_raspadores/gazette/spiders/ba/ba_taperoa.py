from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaTaperoaSpider(BaseDiofSpider):
    TERRITORY_ID = "2931202"
    name = "ba_taperoa"
    website = "https://diario.taperoa.ba.gov.br/homepage"
    start_date = date(2007, 7, 11)
    power = "executive"
