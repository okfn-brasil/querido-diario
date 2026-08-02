from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpDirceReisSpider(BaseDospSpider):
    TERRITORY_ID = "3513850"
    name = "sp_dirce_reis"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/dirce_reis"]
    start_date = date(2019, 4, 4)
