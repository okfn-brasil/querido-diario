from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrTupassiSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4127957"
    name = "pr_tupassi"
    city_subdomain = "tupassi"
    start_date = date(2024, 5, 17)
