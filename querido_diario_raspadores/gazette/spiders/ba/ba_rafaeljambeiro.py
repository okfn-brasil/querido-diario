from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaRafaelJambeiroSpider(BaseDiofSpider):
    TERRITORY_ID = "2925956"
    name = "ba_rafaeljambeiro"
    website = "https://diario.rafaeljambeiro.ba.gov.br/homepage"
    start_date = date(2007, 9, 28)
    power = "executive"
