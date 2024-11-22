import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaSaoLuis(BaseSiganetSpider):
    TERRITORY_ID = "2111300"
    name = "ma_sao_luis"
    start_date = datetime.date(1993, 1, 4)
    allowed_domains = ["diariooficial.saoluis.ma.gov.br"]
    BASE_URL = "https://diariooficial.saoluis.ma.gov.br/dom/dom"
    P_VERSION = "2"  # see BaseSiganetSpider
    P_POWER = "executive"