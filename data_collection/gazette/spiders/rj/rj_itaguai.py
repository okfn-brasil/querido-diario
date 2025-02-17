import datetime as dt

from gazette.spiders.base.modernizacao import BaseModernizacaoSpider


class RjItaguaiSpider(BaseModernizacaoSpider):
    name = "rj_itaguai"
    TERRITORY_ID = "3302007"
    allowed_domains = ["portal.transparencia.itaguai.rj.gov.br"]
    start_date = dt.date(2013, 2, 19)
    power = "executive_legislative"
