from datetime import date

from gazette.spiders.base import SiganetSpider


class MaVianaSpider(SiganetSpider):

    name = "ma_viana"
    allowed_domains = ["transparencia.viana.ma.gov.br"]
    start_date = date(2018, 1, 18)
    url_base = "https://transparencia.viana.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2112803"