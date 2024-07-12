import datetime

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaItapecuruMirimSpider(BaseAdiariosV1Spider):
    name = "ma_itapecuru_mirim"
    allowed_domains = ["itapecurumirim.ma.gov.br"]
    start_date = datetime.date(2023, 1, 2)

    TERRITORY_ID = "2105401"
    BASE_URL = "https://www.itapecurumirim.ma.gov.br"
