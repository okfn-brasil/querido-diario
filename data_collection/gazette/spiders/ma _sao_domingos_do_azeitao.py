from datetime import date

from gazette.spiders.base import SiganetSpider


class MaSaoDomingosDoAzeitaoSpider(SiganetSpider):

    name = "ma_sao_domingos_do_azeitao"
    allowed_domains = ["transparencia.saodomingosdoazeitao.ma.gov.br"]
    start_date = date(2015, 11, 24)
    url_base = "https://transparencia.saodomingosdoazeitao.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2110658"