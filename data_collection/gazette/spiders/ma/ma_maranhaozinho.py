import datetime

from gazette.spiders.base.aratext import BaseAratextSpider


class MaMaranhaozinhoSpider(BaseAratextSpider):
    TERRITORY_ID = "2106375"
    name = "ma_maranhaozinho"
    start_date = datetime.date(2024, 1, 2)
    power = "executive"
    start_urls = ["https://maranhaozinho.ma.gov.br/diariooficial"]
