from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeCaucaiaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2303709"
    name = "ce_caucaia"
    allowed_domains = ["caucaia.ce.gov.br"]
    BASE_URL = "https://www.caucaia.ce.gov.br"
    start_date = date(2002, 6, 3)
