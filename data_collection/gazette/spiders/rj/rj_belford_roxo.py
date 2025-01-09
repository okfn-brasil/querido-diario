from datetime import date

from gazette.spiders.base.modernizacao import BaseModernizacaoSpider


class RjBelfordRoxoSpider(BaseModernizacaoSpider):
    TERRITORY_ID = "3300456"
    name = "rj_belford_roxo"
    allowed_domains = ["transparencia.prefeituradebelfordroxo.rj.gov.br"]
    start_date = date(2019, 1, 2)
    power = "executive"
    edition_endpoint = "WEB-ObterAnexomaior.rule"
    filter_endpoint = "diario_oficial_getmaior"
