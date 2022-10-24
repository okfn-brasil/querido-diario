from datetime import date

from gazette.spiders.base import SiganetSpider


class MaAraiosesSpider(SiganetSpider):

    name = "ma_araioses"
    allowed_domains = ["transparencia.araioses.ma.gov.br"]
    start_date = date(2017, 1, 16)
    url_base = "https://transparencia.araioses.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2100907"