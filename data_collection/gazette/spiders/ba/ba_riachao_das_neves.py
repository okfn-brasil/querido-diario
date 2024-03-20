import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaRiachaoDasNevesSpider(SaiGazetteSpider):
    TERRITORY_ID = "2926202"
    name = "ba_riachao_das_neves"
    start_date = dt.date(2010, 2, 4)
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/riachaodasneves"
