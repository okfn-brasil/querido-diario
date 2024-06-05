from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaValencaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2932903"
    name = "ba_valenca"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/valenca"
    start_date = date(2009, 1, 2)
