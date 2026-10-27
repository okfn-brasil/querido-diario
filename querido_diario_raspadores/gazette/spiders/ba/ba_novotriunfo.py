from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaNovoTriunfoSpider(BaseDiofSpider):
    TERRITORY_ID = "2923050"
    name = "ba_novotriunfo"
    website = "https://diario.novotriunfo.ba.gov.br/homepage"
    start_date = date(2015, 1, 14)
    power = "executive"
