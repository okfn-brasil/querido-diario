from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaTutoiaSpider(SiganetSpider):

    name = "ma_tutoia"
    allowed_domains = ["transparencia.tutoia.ma.gov.br"]
    start_date = date(2017, 1, 5)
    url_base = "https://transparencia.tutoia.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2112506"
