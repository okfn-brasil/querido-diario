from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpPedregulhoSpider(BaseDospSpider):
    TERRITORY_ID = "3537008"
    name = "sp_pedregulho"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/pedregulho"]
    start_date = date(2024, 1, 5)
