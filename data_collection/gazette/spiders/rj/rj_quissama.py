from datetime import date

from gazette.spiders.base.adiarios_v2 import BaseAdiariosV2Spider


class RjQuissamaSpider(BaseAdiariosV2Spider):
    TERRITORY_ID = "3304151"
    name = "rj_quissama"
    allowed_domains = ["quissama.rj.gov.br"]
    BASE_URL = "https://portal.quissama.rj.gov.br"
    start_date = date(2017, 1, 31)
