from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaPenalvaSpider(SiganetSpider):

    name = "ma_penalva"
    allowed_domains = ["transparencia.penalva.ma.gov.br"]
    start_date = date(2021, 4, 22)
    url_base = "https://transparencia.penalva.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2108306"