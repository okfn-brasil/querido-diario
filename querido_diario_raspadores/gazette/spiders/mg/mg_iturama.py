from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MgIturamaSpider(BaseDospSpider):
    TERRITORY_ID = "3134400"
    name = "mg_iturama"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/iturama"]
    start_date = date(2021, 9, 3)
