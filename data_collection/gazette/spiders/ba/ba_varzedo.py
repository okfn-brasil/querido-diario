from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaVarzedoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2933174"
    name = "ba_varzedo"
    allowed_domains = ["varzedo.ba.gov.br"]
    base_url = "https://www.varzedo.ba.gov.br"
    start_date = date(2009, 1, 9)
