import datetime as dt

from gazette.spiders.base.modernizacao import BaseModernizacaoSpider


class RjMesquitaSpider(BaseModernizacaoSpider):
    TERRITORY_ID = "3302858"
    name = "rj_mesquita"
    allowed_domains = ["transparencia.mesquita.rj.gov.br"]
    ver_subpath = "ver20240713"
    start_date = dt.date(2015, 7, 15)
    power = "executive"
