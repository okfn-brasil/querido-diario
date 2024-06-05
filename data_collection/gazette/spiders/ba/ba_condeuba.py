from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCondeubaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2908705"
    name = "ba_condeuba"
    allowed_domains = ["condeuba.ba.gov.br"]
    base_url = "https://www.condeuba.ba.gov.br"
    start_date = date(2011, 1, 12)
