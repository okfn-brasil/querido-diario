import datetime

from gazette.spiders.base.aratext import BaseAratextSpider


class MaCentroDoGuilhermeSpider(BaseAratextSpider):
    TERRITORY_ID = "2103158"
    name = "ma_centro_do_guilherme"
    start_date = datetime.date(2024, 1, 4)
    power = "executive"
    start_urls = ["https://centrodoguilherme.ma.gov.br/diariooficial"]
