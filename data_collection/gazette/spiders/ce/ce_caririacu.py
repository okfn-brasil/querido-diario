from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeCaririacuSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2303204"
    name = "ce_caririacu"
    allowed_domains = ["caririacu.ce.gov.br"]
    BASE_URL = "https://www.caririacu.ce.gov.br"
    start_date = date(2018, 1, 23)
