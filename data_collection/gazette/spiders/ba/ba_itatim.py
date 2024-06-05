from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItatimSpider(SaiGazetteSpider):
    TERRITORY_ID = "2916856"
    name = "ba_itatim"
    allowed_domains = ["itatim.ba.gov.br"]
    base_url = "https://www.itatim.ba.gov.br"
    start_date = date(2009, 1, 7)
