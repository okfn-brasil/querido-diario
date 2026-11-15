from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaRioDoAntonioSpider(BaseDiofSpider):
    TERRITORY_ID = "2926806"
    name = "ba_riodoantonio"
    website = "https://diario.riodoantonio.ba.gov.br/homepage"
    start_date = date(2009, 2, 9)
    power = "executive"
