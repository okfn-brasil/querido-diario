from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpCampoLimpoPaulistaSpider(BaseDospSpider):
    TERRITORY_ID = "3509601"
    name = "sp_campo_limpo_paulista"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/campo_limpo_paulista"]
    start_date = date(2022, 1, 7)
