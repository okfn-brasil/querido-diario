import datetime

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeCaucaiaSpider(BaseAdiariosV1Spider):
    name = "ce_caucaia"
    allowed_domains = ["caucaia.ce.gov.br"]
    start_date = datetime.date(2002, 6, 3)

    TERRITORY_ID = "2303709"
    BASE_URL = "https://www.caucaia.ce.gov.br"
