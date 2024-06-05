from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIbicaraiSpider(SaiGazetteSpider):
    TERRITORY_ID = "2912103"
    name = "ba_ibicarai"
    allowed_domains = ["ibicarai.ba.gov.br"]
    base_url = "https://www.ibicarai.ba.gov.br"
    start_date = date(2007, 9, 5)
