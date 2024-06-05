from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaUbairaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2932101"
    name = "ba_ubaira"
    allowed_domains = ["ubaira.ba.gov.br"]
    base_url = "https://www.ubaira.ba.gov.br"
    start_date = date(2006, 11, 17)
