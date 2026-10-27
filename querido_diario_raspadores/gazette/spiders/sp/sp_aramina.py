from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAraminaSpider(BaseDospSpider):
    TERRITORY_ID = "3503000"
    name = "sp_aramina"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/aramina"]
    start_date = date(2022, 9, 27)
