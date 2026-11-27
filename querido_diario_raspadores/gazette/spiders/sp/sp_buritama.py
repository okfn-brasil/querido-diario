from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBuritamaSpider(BaseDospSpider):
    TERRITORY_ID = "3508108"
    name = "sp_buritama"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/buritama"]
    start_date = date(2019, 10, 22)
