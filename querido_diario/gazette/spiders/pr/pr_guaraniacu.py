from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrGuaraniacuSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4109302"
    name = "pr_guaraniacu"
    city_subdomain = "guaraniacu"
    start_date = date(2021, 5, 3)
