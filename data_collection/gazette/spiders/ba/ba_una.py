from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaUnaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2932507"
    name = "ba_una"
    allowed_domains = ["una.ba.gov.br"]
    base_url = "https://www.una.ba.gov.br"
    start_date = date(2006, 2, 3)
