import datetime as dt

from gazette.spiders.base.modernizacao import BaseModernizacaoSpider


class RjMesquitaSpider(BaseModernizacaoSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "3302858"
    name = "rj_mesquita"
    allowed_domains = ["transparencia.mesquita.rj.gov.br"]
    start_date = dt.date(2015, 7, 15)
    power = "executive"
