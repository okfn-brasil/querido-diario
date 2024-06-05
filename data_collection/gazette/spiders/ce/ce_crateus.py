from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeCrateusSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2304103"
    name = "ce_crateus"
    allowed_domains = ["crateus.ce.gov.br"]
    BASE_URL = "https://www.crateus.ce.gov.br"
    start_date = date(2017, 12, 21)
