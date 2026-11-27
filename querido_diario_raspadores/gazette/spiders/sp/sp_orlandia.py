from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpOrlandiaSpider(BaseDospSpider):
    TERRITORY_ID = "3534302"
    name = "sp_orlandia"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/orlandia"]
    start_date = date(2021, 12, 1)
