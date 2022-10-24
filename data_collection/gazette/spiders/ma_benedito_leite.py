from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaBeneditoLeiteSpider(SiganetSpider):

    name = "ma_benedito_leite"
    allowed_domains = ["transparencia.beneditoleite.ma.gov.br"]
    start_date = date(2017, 12, 13)
    url_base = "https://transparencia.beneditoleite.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2101806"
