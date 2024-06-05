from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIacuSpider(SaiGazetteSpider):
    TERRITORY_ID = "2911907"
    name = "ba_iacu"
    allowed_domains = ["iacu.ba.gov.br"]
    base_url = "https://www.iacu.ba.gov.br"
    start_date = date(2009, 1, 30)
