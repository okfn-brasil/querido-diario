from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaAratacaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2902252"
    name = "ba_arataca"
    allowed_domains = ["arataca.ba.gov.br"]
    base_url = "https://www.arataca.ba.gov.br"
    start_date = date(2005, 1, 13)
