from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaRibeiraDoAmparoSpider(BaseDiofSpider):
    TERRITORY_ID = "2926509"
    name = "ba_ribeiradoamparo"
    website = "https://diario.ribeiradoamparo.ba.gov.br/homepage"
    start_date = date(2007, 12, 13)
    power = "executive"
