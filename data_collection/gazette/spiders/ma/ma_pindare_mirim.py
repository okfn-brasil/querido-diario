from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaPindareMirimSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2108504"
    name = "ma_pindare_mirim"
    allowed_domains = ["pindaremirim.ma.gov.br"]
    BASE_URL = "https://www.pindaremirim.ma.gov.br"
    start_date = date(2020, 1, 2)
