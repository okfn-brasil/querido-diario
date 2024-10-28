from datetime import date

from gazette.spiders.base.sai import BaseSaiSpider


class BaAratacaSpider(BaseSaiSpider):
    TERRITORY_ID = "2902401"
    name = "ba_aurelino_leal"
    allowed_domains = ["aurelinoleal.ba.gov.br"]
    base_url = "https://www.aurelinoleal.ba.gov.br"
    start_date = date(2008, 3, 29)
