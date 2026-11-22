from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaVarzedoSpider(BaseDiofSpider):
    TERRITORY_ID = "2933174"
    name = "ba_varzedo"
    website = "https://diariooficial.varzedo.ba.gov.br/homepage"
    start_date = date(2009, 1, 9)
    end_date = date(2025, 2, 21)
    power = "executive"
