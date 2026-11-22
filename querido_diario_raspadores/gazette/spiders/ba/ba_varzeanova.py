from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaVarzeaNovaSpider(BaseDiofSpider):
    TERRITORY_ID = "2932903"
    name = "ba_varzeanova"
    website = "https://diario.varzeanova.ba.gov.br/homepage"
    start_date = date(2003, 3, 27)
    power = "executive"
