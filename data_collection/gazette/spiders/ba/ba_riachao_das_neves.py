from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaRiachaoDasNevesSpider(BaseDiofSpider):
    TERRITORY_ID = "2926202"
    name = "ba_riachao_das_neves"
    website = "https://sai.io.org.br/ba/riachaodasneves/site/diariooficial"
    start_date = date(2010, 2, 4)
    power = "executive"
