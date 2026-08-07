from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaSantaLuziaDoParuaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2110039"
    name = "ma_santa_luzia_do_parua"
    allowed_domains = ["santaluziadoparua.ma.gov.br"]
    BASE_URL = "https://www.santaluziadoparua.ma.gov.br"
    start_date = date(2023, 11, 24)
