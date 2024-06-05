from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaJussiapeSpider(SaiGazetteSpider):
    TERRITORY_ID = "2918605"
    name = "ba_jussiape"
    allowed_domains = ["jussiape.ba.gov.br"]
    base_url = "https://www.jussiape.ba.gov.br"
    start_date = date(2008, 1, 29)
