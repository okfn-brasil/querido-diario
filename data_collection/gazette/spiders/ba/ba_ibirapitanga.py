from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIbirapitangaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2912707"
    name = "ba_ibirapitanga"
    allowed_domains = ["ibirapitanga.ba.gov.br"]
    base_url = "https://www.ibirapitanga.ba.gov.br"
    start_date = date(2005, 10, 11)
