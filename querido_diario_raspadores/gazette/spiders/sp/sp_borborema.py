from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBorboremaSpider(BaseDospSpider):
    TERRITORY_ID = "3507407"
    name = "sp_borborema"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/borborema"]
    start_date = date(2016, 5, 3)
