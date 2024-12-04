from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaItapecuruMirimSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2105401"
    name = "ma_itapecuru_mirim"
    allowed_domains = ["itapecurumirim.ma.gov.br"]
    BASE_URL = "https://www.itapecurumirim.ma.gov.br"
    start_date = date(2021, 3, 29)
