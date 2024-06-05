from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItabelaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2914653"
    name = "ba_itabela"
    allowed_domains = ["itabela.ba.gov.br"]
    base_url = "https://www.itabela.ba.gov.br"
    start_date = date(2006, 9, 25)
