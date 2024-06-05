from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMaracasSpider(SaiGazetteSpider):
    TERRITORY_ID = "2920502"
    name = "ba_maracas"
    allowed_domains = ["maracas.ba.gov.br"]
    base_url = "https://www.maracas.ba.gov.br"
    start_date = date(2005, 10, 10)
