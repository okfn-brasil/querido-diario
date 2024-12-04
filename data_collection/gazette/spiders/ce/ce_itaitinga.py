from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeItaitingaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2306256"
    name = "ce_itaitinga"
    allowed_domains = ["itaitinga.ce.gov.br"]
    BASE_URL = "https://www.itaitinga.ce.gov.br"
    start_date = date(2018, 4, 25)
