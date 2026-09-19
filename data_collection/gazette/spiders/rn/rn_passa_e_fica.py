from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnPassaEFicaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2409100"
    name = "rn_passa_e_fica"
    allowed_domains = ["passaefica.rn.gov.br"]
    BASE_URL = "https://www.passaefica.rn.gov.br"
    start_date = date(2014, 1, 4)
