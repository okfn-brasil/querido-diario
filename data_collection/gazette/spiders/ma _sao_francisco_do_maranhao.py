from datetime import date

from gazette.spiders.base import SiganetSpider


class MaSaoFranciscoDoMaranhaoSpider(SiganetSpider):

    name = "ma_sao_francisco_do_maranhao"
    allowed_domains = ["transparencia.saofranciscodomaranhao.ma.gov.br"]
    start_date = date(2017, 3, 22)
    url_base = "https://transparencia.saofranciscodomaranhao.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2110906"