from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaAurelinoLealSpider(SaiGazetteSpider):
    TERRITORY_ID = "2902401"
    name = "ba_aurelino_leal"
    allowed_domains = ["aurelinoleal.ba.gov.br"]
    base_url = "https://www.aurelinoleal.ba.gov.br"
    start_date = date(2016, 1, 4)
