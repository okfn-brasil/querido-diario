from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSantaLuziaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2928059"
    name = "ba_santa_luzia_2024"
    allowed_domains = ["santaluzia.ba.gov.br"]
    base_url = "https://www.santaluzia.ba.gov.br"
    start_date = date(2024, 1, 5)
