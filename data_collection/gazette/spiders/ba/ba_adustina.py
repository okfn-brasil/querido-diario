from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaAdustinaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2900355"
    name = "ba_adustina"
    allowed_domains = ["adustina.ba.gov.br"]
    base_url = "https://www.adustina.ba.gov.br"
    start_date = date(2017, 1, 3)
