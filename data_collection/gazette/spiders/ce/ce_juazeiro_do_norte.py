import datetime

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeJuazeiroDoNorteSpider(BaseAdiariosV1Spider):
    name = "ce_juazeiro_do_norte"
    allowed_domains = ["juazeirodonorte.ce.gov.br"]
    start_date = datetime.date(2021, 1, 12)

    TERRITORY_ID = "2307304"
    BASE_URL = "https://www.juazeirodonorte.ce.gov.br"
