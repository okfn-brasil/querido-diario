from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaOlhoDAguaDasCunhasSpider(SiganetSpider):

    name = "ma_olho_dagua_das_cunhas"
    allowed_domains = ["transparencia.olhodaguadascunhas.ma.gov.br"]
    start_date = date(2019, 11, 1)
    url_base = "https://transparencia.olhodaguadascunhas.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2107407"