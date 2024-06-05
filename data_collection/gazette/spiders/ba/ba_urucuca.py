from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaUrucucaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2932705"
    name = "ba_urucuca"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/urucuca"
    start_date = date(2005, 8, 18)
