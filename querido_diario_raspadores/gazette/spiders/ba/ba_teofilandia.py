from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaTeofilandiaSpider(BaseDiofSpider):
    TERRITORY_ID = "2931509"
    name = "ba_teofilandia"
    website = "https://diario.teofilandia.ba.gov.br/homepage"
    start_date = date(2010, 1, 7)
    power = "executive"
