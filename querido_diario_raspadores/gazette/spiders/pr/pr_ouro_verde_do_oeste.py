from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrOuroVerdeDoOesteSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4117453"
    name = "pr_ouro_verde_do_oeste"
    city_subdomain = "ouroverdedooeste"
    start_date = date(2021, 3, 31)
