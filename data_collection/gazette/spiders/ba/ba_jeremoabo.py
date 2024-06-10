from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaJeremoaboSpider(SaiGazetteSpider):
    TERRITORY_ID = "2918100"
    name = "ba_jeremoabo"
    allowed_domains = ["jeremoabo.ba.gov.br"]
    base_url = "https://www.jeremoabo.ba.gov.br"
    start_date = date(2010, 7, 8)
