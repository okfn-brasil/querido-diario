from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaRibeiraoDoLargoSpider(BaseDiofSpider):
    TERRITORY_ID = "2926657"
    name = "ba_ribeiraodolargo"
    website = "https://diario.ribeiraodolargo.ba.gov.br/homepage"
    start_date = date(2013, 1, 5)
    power = "executive"
