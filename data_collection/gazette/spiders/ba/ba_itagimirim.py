from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItagimirimSpider(SaiGazetteSpider):
    TERRITORY_ID = "2915304"
    name = "ba_itagimirim"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/itagimirim"
    start_date = date(2005, 7, 8)
