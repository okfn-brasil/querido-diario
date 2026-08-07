from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeLimoeiroDoNorteSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2307601"
    name = "ce_limoeiro_do_norte"
    allowed_domains = ["limoeirodonorte.ce.gov.br"]
    BASE_URL = "https://www.limoeirodonorte.ce.gov.br"
    start_date = date(2017, 4, 10)
