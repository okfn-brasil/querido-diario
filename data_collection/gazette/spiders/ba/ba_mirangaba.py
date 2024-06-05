from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMirangabaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2921401"
    name = "ba_mirangaba"
    allowed_domains = ["mirangaba.ba.gov.br"]
    base_url = "https://www.mirangaba.ba.gov.br"
    start_date = date(2009, 1, 16)
