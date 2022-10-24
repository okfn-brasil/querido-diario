from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaCarolinaSpider(SiganetSpider):

    name = "ma_carolina"
    allowed_domains = ["transparencia.carolina.ma.gov.br"]
    start_date = date(2015, 11, 25)
    url_base = "https://transparencia.carolina.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2102804"