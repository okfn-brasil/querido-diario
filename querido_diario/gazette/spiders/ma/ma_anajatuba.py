from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaAnajatubaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2100709"
    name = "ma_anajatuba"
    allowed_domains = ["anajatuba.ma.gov.br"]
    BASE_URL = "https://www.anajatuba.ma.gov.br"
    start_date = date(2021, 2, 12)
