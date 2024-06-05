from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaAnageSpider(SaiGazetteSpider):
    TERRITORY_ID = "2901205"
    name = "ba_anage"
    allowed_domains = ["anage.ba.gov.br"]
    base_url = "https://www.anage.ba.gov.br"
    start_date = date(2007, 1, 12)
