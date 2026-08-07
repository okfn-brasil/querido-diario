from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeMilagresSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2308302"
    name = "ce_milagres"
    allowed_domains = ["milagres.ce.gov.br"]
    BASE_URL = "https://www.milagres.ce.gov.br"
    start_date = date(2016, 5, 20)
