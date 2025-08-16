from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeUruocaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2313906"
    name = "ce_uruoca"
    allowed_domains = ["uruoca.ce.gov.br"]
    BASE_URL = "https://www.uruoca.ce.gov.br"
    start_date = date(2017, 1, 2)
