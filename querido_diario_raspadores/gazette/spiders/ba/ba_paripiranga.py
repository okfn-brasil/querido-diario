from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaParipirangaSpider(BaseDiofSpider):
    TERRITORY_ID = "2923803"
    name = "ba_paripiranga"
    website = "https://diario.paripiranga.ba.gov.br/homepage"
    start_date = date(2008, 1, 22)
    power = "executive"
