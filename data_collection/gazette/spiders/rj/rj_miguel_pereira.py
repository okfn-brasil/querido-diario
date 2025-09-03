import datetime as dt

from gazette.spiders.base.modernizacao import BaseModernizacaoSpider


class RjMiguelPereiraSpider(BaseModernizacaoSpider):
    TERRITORY_ID = "3302908"
    name = "rj_miguel_pereira"
    allowed_domains = ["transparencia.miguelpereira.rj.gov.br"]
    start_date = dt.date(2021, 9, 3)
