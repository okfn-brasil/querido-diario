from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaChorrochoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2907707"
    name = "ba_chorrocho"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/chorrocho"
    start_date = date(2009, 1, 30)
