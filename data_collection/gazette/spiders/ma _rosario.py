from datetime import date

from gazette.spiders.base import SiganetSpider


class MaRosarioSpider(SiganetSpider):

    name = "ma_rosario"
    allowed_domains = ["transparencia.rosario.ma.gov.br"]
    start_date = date(2021, 1, 4)
    url_base = "https://transparencia.rosario.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2109601"