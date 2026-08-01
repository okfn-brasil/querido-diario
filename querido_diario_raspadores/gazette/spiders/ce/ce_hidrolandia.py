from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeHidrolandiaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2305209"
    name = "ce_hidrolandia"
    allowed_domains = ["hidrolandia.ce.gov.br"]
    BASE_URL = "https://www.hidrolandia.ce.gov.br"
    start_date = date(2007, 4, 9)
