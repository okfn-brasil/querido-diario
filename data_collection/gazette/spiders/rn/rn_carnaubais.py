from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnCarnaubaisSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2402501"
    name = "rn_carnaubais"
    allowed_domains = ["carnaubais.rn.gov.br"]
    BASE_URL = "https://www.carnaubais.rn.gov.br"
    start_date = date(2017, 1, 5)
