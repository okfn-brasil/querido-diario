from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBuritizalSpider(BaseDospSpider):
    TERRITORY_ID = "3508207"
    name = "sp_buritizal"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/buritizal"]
    start_date = date(2022, 10, 26)
