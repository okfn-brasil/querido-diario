from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpJaguariunaSpider(BaseDospSpider):
    TERRITORY_ID = "3524709"
    name = "sp_jaguariuna"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/jaguariuna"]
    start_date = date(2019, 3, 8)
