from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpItupevaSpider(BaseDospSpider):
    TERRITORY_ID = "3524006"
    name = "sp_itupeva"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/itupeva"]
    start_date = date(2019, 9, 24)
