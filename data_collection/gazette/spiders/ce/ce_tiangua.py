from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeTianguaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2313401"
    name = "ce_tiangua"
    allowed_domains = ["tiangua.ce.gov.br"]
    BASE_URL = "https://www.tiangua.ce.gov.br"
    start_date = date(2021, 11, 3)
