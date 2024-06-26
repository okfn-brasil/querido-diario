from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrAraucariaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4101804"
    name = "pr_araucaria"
    city_subdomain = "araucaria"
    start_date = date(2024, 5, 24)
