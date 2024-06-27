from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeAuroraSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2301703"
    name = "ce_aurora"
    allowed_domains = ["aurora.ce.gov.br"]
    BASE_URL = "https://www.aurora.ce.gov.br"
    start_date = date(2021, 8, 2)
