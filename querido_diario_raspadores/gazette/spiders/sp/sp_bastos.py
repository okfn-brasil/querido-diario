from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBastosSpider(BaseDospSpider):
    TERRITORY_ID = "3505807"
    name = "sp_bastos"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/bastos"]
    start_date = date(2022, 3, 17)
