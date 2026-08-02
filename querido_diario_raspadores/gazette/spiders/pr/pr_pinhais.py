from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrPinhaisSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4119152"
    name = "pr_pinhais"
    city_subdomain = "pinhais"
    start_date = date(2017, 5, 26)
