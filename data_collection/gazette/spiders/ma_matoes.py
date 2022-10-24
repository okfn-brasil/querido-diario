from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaMatoesSpider(SiganetSpider):

    name = "ma_matoes"
    allowed_domains = ["transparencia.matoes.ma.gov.br"]
    start_date = date(2021, 11, 25)
    url_base = "https://transparencia.matoes.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2106607"
