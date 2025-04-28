from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaPedreirasSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2108207"
    name = "ma_pedreiras"
    allowed_domains = ["pedreiras.ma.gov.br"]
    BASE_URL = "https://www.pedreiras.ma.gov.br"
    start_date = date(2015, 2, 20)
