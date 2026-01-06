from datetime import date

from gazette.spiders.base.adiarios_v2 import BaseAdiariosV2Spider


class RjCasimiroDeAbreuSpider(BaseAdiariosV2Spider):
    TERRITORY_ID = "3301306"
    name = "rj_casimiro_de_abreu"
    allowed_domains = ["casimirodeabreu.rj.gov.br"]
    BASE_URL = "https://www.transparencia.casimirodeabreu.rj.gov.br"
    start_date = date(2017, 1, 4)
