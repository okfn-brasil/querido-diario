from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaBacabeiraSpider(SiganetSpider):

    name = "ma_bacabeira"
    allowed_domains = ["transparencia.bacabeira.ma.gov.br"]
    start_date = date(2015, 10, 23)
    url_base = "https://transparencia.bacabeira.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2101251"
