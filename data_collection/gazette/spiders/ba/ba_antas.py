from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaAntasSpider(BaseDiofSpider):
    TERRITORY_ID = "2901601"
    name = "ba_antas"
    website = "https://diario.antas.ba.gov.br/"
    start_date = date(2013, 2, 21)
    power = "executive"
