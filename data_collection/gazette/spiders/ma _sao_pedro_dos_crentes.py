from datetime import date

from gazette.spiders.base import SiganetSpider


class MaSaoPedroDosCrentesSpider(SiganetSpider):

    name = "ma_sao_pedro_dos_crentes"
    allowed_domains = ["transparencia.saopedrodoscrentes.ma.gov.br"]
    start_date = date(2020, 1, 22)
    url_base = "https://transparencia.saopedrodoscrentes.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2111573"