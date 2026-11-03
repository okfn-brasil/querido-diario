from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBalsamoSpider(BaseDospSpider):
    TERRITORY_ID = "3504800"
    name = "sp_balsamo"
    start_urls = ["https://imprensaoficialmunicipal.com.br/balsamo"]
    start_date = date(2017, 2, 22)
