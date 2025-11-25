from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class CeHorizonteSpider(BaseDospSpider):
    TERRITORY_ID = "2305233"
    name = "ce_horizonte"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/horizonte"]
    start_date = date(2023, 7, 3)
