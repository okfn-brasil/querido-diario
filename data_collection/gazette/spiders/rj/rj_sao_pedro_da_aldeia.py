import datetime as dt

from gazette.spiders.base.modernizacao import BaseModernizacaoSpider


class RjSaoPedroDaAldeiaSpider(BaseModernizacaoSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "3305208"
    name = "rj_sao_pedro_da_aldeia"
    allowed_domains = ["transparencia.pmspa.rj.gov.br"]
    start_date = dt.date(2018, 1, 15)
    ver_subpath = "ver20240713"
