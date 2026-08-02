import datetime as dt

from gazette.spiders.base.modernizacao import BaseModernizacaoSpider


class RjSaoJoaoDeMeritiSpider(BaseModernizacaoSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "3305109"
    name = "rj_sao_joao_de_meriti"
    allowed_domains = ["transparencia.meriti.rj.gov.br"]
    start_date = dt.date(2017, 1, 1)
