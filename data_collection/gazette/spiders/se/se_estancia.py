from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class SeEstanciaSpider(BaseDiofSpider):
    TERRITORY_ID = "2802106"
    name = "se_estancia"
    website = "https://diario.estancia.se.gov.br"
    start_date = date(2016, 4, 28)
    power = "executive"
