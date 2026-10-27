from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAnalandiaSpider(BaseDospSpider):
    TERRITORY_ID = "3502002"
    name = "sp_analandia"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/analandia"]
    start_date = date(2022, 11, 11)
