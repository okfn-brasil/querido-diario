from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaMaracacumeSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2106326"
    name = "ma_maracacume"
    allowed_domains = ["maracacume.ma.gov.br"]
    BASE_URL = "https://www.maracacume.ma.gov.br"
    start_date = date(2019, 10, 20)
