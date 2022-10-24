from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaPaulinoNevesSpider(SiganetSpider):

    name = "ma_paulino_neves"
    allowed_domains = ["transparencia.paulinoneves.ma.gov.br"]
    start_date = date(2021, 1, 21)
    url_base = "https://transparencia.paulinoneves.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2108058"