import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaMaranhaozinho(BaseSiganetSpider):
    TERRITORY_ID = "2106375"
    name = "ma_maranhaozinho"
    start_date = datetime.date(2021, 1, 26)
    allowed_domains = ["transparencia.maranhaozinho.ma.gov.br"]
    BASE_URL = (
        "https://transparencia.maranhaozinho.ma.gov.br/acessoInformacao/diario/diario"
    )
