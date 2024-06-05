from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItapeSpider(SaiGazetteSpider):
    TERRITORY_ID = "2916203"
    name = "ba_itape"
    allowed_domains = ["itape.ba.gov.br"]
    base_url = "https://www.itape.ba.gov.br"
    start_date = date(2008, 7, 10)
