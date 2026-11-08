from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaPalmeirasSpider(BaseDiofSpider):
    TERRITORY_ID = "2923506"
    name = "ba_palmeiras"
    website = "https://diario.palmeiras.ba.gov.br/homepage"
    start_date = date(2006, 4, 24)
    power = "executive"
