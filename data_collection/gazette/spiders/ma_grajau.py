from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaGrajauSpider(SiganetSpider):

    name = "ma_grajau"
    allowed_domains = ["transparencia.grajau.ma.gov.br"]
    start_date = date(2021, 5, 6)
    url_base = "https://transparencia.grajau.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2104800"