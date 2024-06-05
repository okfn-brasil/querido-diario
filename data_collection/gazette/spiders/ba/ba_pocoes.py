from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPocoesSpider(SaiGazetteSpider):
    TERRITORY_ID = "2925105"
    name = "ba_pocoes"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/pocoes"
    start_date = date(2009, 1, 6)
