from datetime import date

from gazette.spiders.base.sai import BaseSaiSpider


class BaAracasSpider(BaseSaiSpider):
    TERRITORY_ID = "2902054"
    name = "ba_aracas"
    allowed_domains = ["aracas.ba.gov.br"]
    base_url = "https://www.aracas.ba.gov.br"
    start_date = date(2014, 11, 27)
