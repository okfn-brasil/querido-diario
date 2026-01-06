from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpItuSpider(BaseDospSpider):
    TERRITORY_ID = "3523909"
    name = "sp_itu"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/itu"]
    start_date = date(2019, 8, 15)
