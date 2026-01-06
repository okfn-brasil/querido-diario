from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpItapevaSpider(BaseDospSpider):
    TERRITORY_ID = "3522406"
    name = "sp_itapeva"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/itapeva"]
    start_date = date(2017, 12, 18)
