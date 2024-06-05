from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItororoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2917102"
    name = "ba_itororo"
    allowed_domains = ["itororo.ba.gov.br"]
    base_url = "https://www.itororo.ba.gov.br"
    start_date = date(2006, 6, 20)
