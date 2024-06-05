from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaOurolandiaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2923357"
    name = "ba_ourolandia"
    allowed_domains = [".ourolandia.ba.gov.br"]
    base_url = "https://diariooficial.ourolandia.ba.gov.br"
    start_date = date(2014, 2, 7)
