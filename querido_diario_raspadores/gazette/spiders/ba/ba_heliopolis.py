from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaHeliopolisSpider(BaseDiofSpider):
    TERRITORY_ID = "2911857"
    name = "ba_heliopolis"
    website = "https://diario.heliopolis.ba.gov.br/homepage"
    start_date = date(2009, 2, 17)
    power = "executive"
