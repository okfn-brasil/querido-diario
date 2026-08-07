from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaMatoesDoNorteSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2106631"
    name = "ma_matoes_do_norte"
    allowed_domains = ["matoesdonorte.ma.gov.br"]
    BASE_URL = "https://www.matoesdonorte.ma.gov.br"
    start_date = date(2010, 3, 29)
