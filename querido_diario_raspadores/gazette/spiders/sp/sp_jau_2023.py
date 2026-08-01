from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpJauSpider_2023(BaseDospSpider):
    TERRITORY_ID = "3525300"
    name = "sp_jau_2023"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/jau"]
    start_date = date(2023, 1, 6)
