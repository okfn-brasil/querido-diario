from datetime import date

from gazette.spiders.base.adiarios_v2 import BaseAdiariosV2Spider


class RjCordeiroSpider(BaseAdiariosV2Spider):
    TERRITORY_ID = "3301504"
    name = "rj_cordeiro"
    allowed_domains = ["cordeiro.rj.gov.br"]
    BASE_URL = "https://www.transparencia.cordeiro.rj.gov.br"
    start_date = date(2017, 10, 5)
