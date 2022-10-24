from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaFeiraNovaDoMaranhaoSpider(SiganetSpider):

    name = "ma_feira_nova_do_maranhao"
    allowed_domains = ["transparencia.feiranovadomaranhao.ma.gov.br"]
    start_date = date(2017, 1, 31)
    url_base = "https://transparencia.feiranovadomaranhao.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2104073"