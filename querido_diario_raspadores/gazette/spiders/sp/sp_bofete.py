from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBofeteSpider(BaseDospSpider):
    TERRITORY_ID = "3506904"
    name = "sp_bofete"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/bofete"]
    start_date = date(2021, 5, 24)
