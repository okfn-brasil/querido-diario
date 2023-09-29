import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaAxixa(BaseSiganetSpider):
    TERRITORY_ID = "2101103"
    name = "ma_axixa"
    start_date = datetime.date(2021, 3, 31)
    allowed_domains = ["transparencia.axixa.ma.gov.br"]
    BASE_URL = "https://transparencia.axixa.ma.gov.br/acessoInformacao/diario/diario"
