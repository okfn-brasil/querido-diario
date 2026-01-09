import datetime as dt

from gazette.spiders.base.modernizacao import BaseModernizacaoSpider


class RjDuqueDeCaxiasSpider(BaseModernizacaoSpider):
    zyte_smartproxy_enabled = True

    name = "rj_duque_de_caxias"
    TERRITORY_ID = "3301702"
    allowed_domains = ["transparencia.duquedecaxias.rj.gov.br"]
    start_date = dt.date(2017, 1, 2)
