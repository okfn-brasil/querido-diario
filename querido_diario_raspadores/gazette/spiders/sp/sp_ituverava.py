from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpItuveravaSpider(BaseDospSpider):
    TERRITORY_ID = "3524105"
    name = "sp_ituverava"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/ituverava"]
    start_date = date(2022, 12, 8)
