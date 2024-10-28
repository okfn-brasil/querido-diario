from datetime import date

from gazette.spiders.base.sai import BaseSaiSpider


class BaAratacaSpider(BaseSaiSpider):
    TERRITORY_ID = "2902906"
    name = "ba_barra_do_choca"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/barradochoca"
    start_date = date(2009, 1, 5)
