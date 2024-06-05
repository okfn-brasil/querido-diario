from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItapitangaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2916609"
    name = "ba_itapitanga"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/itapitanga"
    start_date = date(2009, 1, 13)
