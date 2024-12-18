from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class ApTartarugalzinhoSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "1600709"
    name = "ap_tartarugalzinho"
    allowed_domains = ["tartarugalzinho.ap.gov.br"]
    BASE_URL = "https://www.tartarugalzinho.ap.gov.br"
    start_date = date(2017, 5, 16)
