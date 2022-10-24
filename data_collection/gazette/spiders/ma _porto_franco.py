from datetime import date

from gazette.spiders.base import SiganetSpider


class MaPortoFrancoSpider(SiganetSpider):

    name = "ma_porto_franco"
    allowed_domains = ["transparencia.portofranco.ma.gov.br"]
    start_date = date(2016, 1, 12)
    url_base = "https://transparencia.portofranco.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2109007"