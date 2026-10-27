from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpArealvaSpider(BaseDospSpider):
    TERRITORY_ID = "3503406"
    name = "sp_arealva"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/arealva"]
    start_date = date(2017, 10, 9)
