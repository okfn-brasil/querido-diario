from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PaGarrafaoDoNorteSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "1503077"
    name = "pa_garrafao_do_norte"
    allowed_domains = ["garrafaodonorte.pa.gov.br"]
    BASE_URL = "https://www.garrafaodonorte.pa.gov.br"
    start_date = date(2018, 7, 31)
