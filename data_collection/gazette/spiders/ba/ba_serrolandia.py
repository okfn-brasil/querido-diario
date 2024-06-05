from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSerrolandiaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2930600"
    name = "ba_serrolandia"
    allowed_domains = ["serrolandia.ba.gov.br"]
    base_url = "https://www.serrolandia.ba.gov.br"
    start_date = date(2008, 1, 17)
