from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBragancaPaulistaSpider(BaseDospSpider):
    TERRITORY_ID = "3507605"
    name = "sp_braganca_paulista"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/braganca_paulista"]
    start_date = date(2019, 1, 4)
