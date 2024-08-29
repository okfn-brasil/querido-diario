from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaBuriticupuSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2102325"
    name = "ma_buriticupu"
    allowed_domains = ["buriticupu.ma.gov.br"]
    BASE_URL = "https://www.buriticupu.ma.gov.br"
    start_date = date(2018, 5, 7)
