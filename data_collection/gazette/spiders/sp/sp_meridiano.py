from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpMeridianoSpider(BaseDospSpider):
    TERRITORY_ID = "3529609"
    name = "sp_meridiano"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/meridiano"]
    start_date = date(2014, 10, 23)
