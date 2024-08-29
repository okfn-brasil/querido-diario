from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeCoreauSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2304004"
    name = "ce_coreau"
    allowed_domains = ["coreau.ce.gov.br"]
    BASE_URL = "https://www.coreau.ce.gov.br"
    start_date = date(2024, 5, 3)
