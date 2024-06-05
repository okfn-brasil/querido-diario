from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIchuSpider(SaiGazetteSpider):
    TERRITORY_ID = "2913309"
    name = "ba_ichu"
    allowed_domains = ["ichu.ba.gov.br"]
    base_url = "https://www.ichu.ba.gov.br"
    start_date = date(2023, 1, 6)
