import datetime

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaBuriticupuSpider(BaseAdiariosV1Spider):
    name = "ma_buriticupu"
    allowed_domains = ["buriticupu.ma.gov.br"]
    start_date = datetime.date(2018, 5, 7)

    TERRITORY_ID = "2102325"
    BASE_URL = "https://www.buriticupu.ma.gov.br"
