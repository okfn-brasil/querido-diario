from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MgItajubaSpider(BaseDospSpider):
    TERRITORY_ID = "3132404"
    name = "mg_itajuba"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/itajuba"]
    start_date = date(2023, 5, 15)
