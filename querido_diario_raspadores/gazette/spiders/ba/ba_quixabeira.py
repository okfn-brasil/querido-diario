from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaQuixabeiraSpider(BaseDiofSpider):
    TERRITORY_ID = "2925931"
    name = "ba_quixabeira"
    website = "https://diario.quixabeira.ba.gov.br/homepage"
    start_date = date(2007, 10, 23)
    power = "executive"
