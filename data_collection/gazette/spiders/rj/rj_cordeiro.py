from datetime import date

from gazette.spiders.base.adiarios_v2 import BaseAdiariosV2Spider


class RjCordeiroSpider(BaseAdiariosV2Spider):
    name = "rj_cordeiro"
    TERRITORY_ID = "3301504"
    start_date = date(2017, 10, 5)
    allowed_domains = ["cordeiro.rj.gov.br"]
    BASE_URL = "https://transparencia.cordeiro.rj.gov.br"
