from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnSantaCruzSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2411205"
    name = "rn_santa_cruz"
    allowed_domains = ["santacruz.rn.gov.br"]
    BASE_URL = "https://www.santacruz.rn.gov.br"
    start_date = date(2022, 1, 4)
