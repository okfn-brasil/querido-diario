from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaFortalezaDosNogueirasSpider(SiganetSpider):

    name = "ma_fortaleza_dos_nogueiras"
    allowed_domains = ["transparencia.fortalezadosnogueiras.ma.gov.br"]
    start_date = date(2017, 1, 19)
    url_base = "https://transparencia.fortalezadosnogueiras.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2104107"