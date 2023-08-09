import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaAfonsoCunha(BaseSiganetSpider):
    TERRITORY_ID = "2100105"
    name = "ma_afonso_cunha"
    start_date = datetime.date(2020, 7, 30)
    allowed_domains = ["transparencia.afonsocunha.ma.gov.br"]
    BASE_URL = (
        "https://transparencia.afonsocunha.ma.gov.br/acessoInformacao/diario/diario"
    )
