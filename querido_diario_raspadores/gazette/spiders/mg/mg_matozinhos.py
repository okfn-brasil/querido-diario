from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MgMatozinhosSpider(BaseDospSpider):
    TERRITORY_ID = "3141108"
    name = "mg_matozinhos"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/matozinhos"]
    start_date = date(2020, 4, 2)
