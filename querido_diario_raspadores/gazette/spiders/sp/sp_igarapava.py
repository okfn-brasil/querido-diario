from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpIgarapavaSpider(BaseDospSpider):
    TERRITORY_ID = "3520103"
    name = "sp_igarapava"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/igarapava"]
    start_date = date(2019, 10, 10)
