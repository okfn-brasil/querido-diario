from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpSertaozinhoSpider(BaseDospSpider):
    TERRITORY_ID = "3551702"
    name = "sp_sertaozinho"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/sertaozinho"]
    start_date = date(2019, 8, 7)
