from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeSaoBeneditoSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2312304"
    name = "ce_sao_benedito"
    allowed_domains = ["saobenedito.ce.gov.br"]
    BASE_URL = "https://www.saobenedito.ce.gov.br"
    start_date = date(18, 2, 15)
