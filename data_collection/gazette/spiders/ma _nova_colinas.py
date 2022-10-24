from datetime import date

from gazette.spiders.base import SiganetSpider


class MaNovaColinasSpider(SiganetSpider):

    name = "ma_nova_colinas"
    allowed_domains = ["transparencia.novacolinas.ma.gov.br"]
    start_date = date(2015, 3, 4)
    url_base = "https://transparencia.novacolinas.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2107258"