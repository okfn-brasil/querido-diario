from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpCunhaSpider(BaseDospSpider):
    TERRITORY_ID = "3513603"
    name = "sp_cunha"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/cunha"]
    start_date = date(2021, 10, 19)
