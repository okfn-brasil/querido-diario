from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaNovaVicosaSpider(BaseDiofSpider):
    TERRITORY_ID = "2923001"
    name = "ba_novavicosa"
    website = "https://diario.novavicosa.ba.gov.br/homepage"
    start_date = date(2007, 12, 17)
    power = "executive"
