from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpHolambraSpider(BaseDospSpider):
    TERRITORY_ID = "3519055"
    name = "sp_holambra"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/holambra"]
    start_date = date(2017, 5, 3)
