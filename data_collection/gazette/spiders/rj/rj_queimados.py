import datetime as dt

from gazette.spiders.base.modernizacao import BaseModernizacaoSpider


class RjQueimadosSpider(BaseModernizacaoSpider):
    zyte_smartproxy_enabled = False

    TERRITORY_ID = "3304144"
    name = "rj_queimados"
    allowed_domains = ["transparencia.queimados.rj.gov.br"]
    start_date = dt.date(2018, 1, 3)
