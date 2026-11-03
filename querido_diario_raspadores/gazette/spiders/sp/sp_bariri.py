from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBaririSpider(BaseDospSpider):
    TERRITORY_ID = "3505203"
    name = "sp_bariri"
    start_urls = ["https://imprensaoficialmunicipal.com.br/bariri"]
    start_date = date(2017, 12, 13)
