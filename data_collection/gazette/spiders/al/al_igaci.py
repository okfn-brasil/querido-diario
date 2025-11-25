from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class AlIgaciSpider(BaseDiofSpider):
    TERRITORY_ID = "2703106"
    name = "al_igaci"
    website = "https://diario.igaci.al.gov.br"
    start_date = date(2015, 7, 17)
    power = "executive"
