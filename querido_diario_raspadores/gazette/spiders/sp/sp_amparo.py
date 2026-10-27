from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAmparoSpider(BaseDospSpider):
    TERRITORY_ID = "3501905"
    name = "sp_amparo"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/amparo"]
    start_date = date(2019, 10, 18)
