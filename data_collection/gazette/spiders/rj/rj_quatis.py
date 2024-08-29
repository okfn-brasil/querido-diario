import datetime as dt

from gazette.spiders.base.modernizacao import BaseModernizacaoSpider


class RjQuatisSpider(BaseModernizacaoSpider):
    TERRITORY_ID = "3304128"
    name = "rj_quatis"
    allowed_domains = ["transparencia.quatis.rj.gov.br"]
    start_date = dt.date(2021, 1, 11)
