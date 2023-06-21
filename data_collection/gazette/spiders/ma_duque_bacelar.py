import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaDuqueBacelar(BaseSiganetSpider):
    TERRITORY_ID = "2103901"
    name = "ma_duque_bacelar"
    start_date = datetime.date(2018, 6, 1)
    allowed_domains = ["transparencia.duquebacelar.ma.gov.br"]
    BASE_URL = "https://transparencia.duquebacelar.ma.gov.br/acessoInformacao/diario/diario"
