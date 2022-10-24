from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaCoroataSpider(SiganetSpider):

    name = "ma_coroata"
    allowed_domains = ["transparencia.coroata.ma.gov.br"]
    start_date = date(2017, 7, 28)
    url_base = "https://transparencia.coroata.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2103604"
