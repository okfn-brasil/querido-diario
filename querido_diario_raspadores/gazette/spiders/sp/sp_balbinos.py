from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBalbinosSpider(BaseDospSpider):
    TERRITORY_ID = "3504701"
    name = "sp_balbinos"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/balbinos"]
    start_date = date(2018, 2, 2)
