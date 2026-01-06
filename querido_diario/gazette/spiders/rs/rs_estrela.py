from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsEstrelaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4307807"
    name = "rs_estrela"
    city_subdomain = "estrela"
    start_date = date(2021, 3, 29)
