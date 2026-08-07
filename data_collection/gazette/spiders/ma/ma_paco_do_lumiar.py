from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaPacoDoLumiarSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2107506"
    name = "ma_paco_do_lumiar"
    allowed_domains = ["pacodolumiar.ma.gov.br"]
    BASE_URL = "https://www.pacodolumiar.ma.gov.br"
    start_date = date(2017, 8, 3)
