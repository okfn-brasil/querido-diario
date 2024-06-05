from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMacurureSpider(SaiGazetteSpider):
    TERRITORY_ID = "2919900"
    name = "ba_macurure"
    allowed_domains = ["macurure.ba.gov.br"]
    base_url = "https://www.macurure.ba.gov.br"
    start_date = date(2006, 6, 6)
