from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpHerculandiaSpider(BaseDospSpider):
    TERRITORY_ID = "3519006"
    name = "sp_herculandia"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/herculandia"]
    start_date = date(2020, 1, 31)
