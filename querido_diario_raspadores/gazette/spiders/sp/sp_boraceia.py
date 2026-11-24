from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBoraceiaSpider(BaseDospSpider):
    TERRITORY_ID = "3507308"
    name = "sp_boraceia"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/boraceia"]
    start_date = date(2024, 2, 5)
