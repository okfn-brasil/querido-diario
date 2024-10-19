from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnSaoFranciscoDoOesteSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2411908"
    name = "rn_sao_francisco_do_oeste"
    allowed_domains = ["saofranciscodooeste.rn.gov.br"]
    BASE_URL = "https://www.saofranciscodooeste.rn.gov.br"
    start_date = date(2023, 2, 7)
