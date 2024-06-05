from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPlanaltoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2925006"
    name = "ba_planalto"
    allowed_domains = ["planalto.ba.gov.br"]
    base_url = "https://www.planalto.ba.gov.br"
    start_date = date(2017, 1, 6)
