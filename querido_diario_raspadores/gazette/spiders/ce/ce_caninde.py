from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeCanindeSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2302800"
    name = "ce_caninde"
    allowed_domains = ["caninde.ce.gov.br"]
    BASE_URL = "https://www.caninde.ce.gov.br"
    start_date = date(2017, 8, 3)
