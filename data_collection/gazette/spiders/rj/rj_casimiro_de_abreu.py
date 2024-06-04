from datetime import date

from gazette.spiders.base.adiarios_v2 import BaseAdiariosV2Spider


class RjCasimiroDeAbreuSpider(BaseAdiariosV2Spider):
    name = "rj_casimiro_de_abreu"
    TERRITORY_ID = "3301306"
    start_date = date(2017, 1, 4)
    allowed_domains = ["casimirodeabreu.rj.gov.br"]
    BASE_URL = "https://transparencia.casimirodeabreu.rj.gov.br"
