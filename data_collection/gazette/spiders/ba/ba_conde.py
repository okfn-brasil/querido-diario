from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCondeSpider(SaiGazetteSpider):
    TERRITORY_ID = "2908606"
    name = "ba_conde"
    allowed_domains = ["conde.ba.gov.br"]
    base_url = "https://www.conde.ba.gov.br"
    start_date = date(2021, 1, 4)
