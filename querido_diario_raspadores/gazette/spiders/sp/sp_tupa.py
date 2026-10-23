from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpTupaSpider(BaseDospSpider):
    TERRITORY_ID = "3555000"
    name = "sp_tupa"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/tupa"]
    start_date = date(2021, 10, 2)
