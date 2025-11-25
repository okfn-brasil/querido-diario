from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpSaltoSpider(BaseDospSpider):
    TERRITORY_ID = "3545209"
    name = "sp_salto"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/salto"]
    start_date = date(2018, 2, 1)
