from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrApucaranaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4101408"
    name = "pr_apucarana"
    city_subdomain = "apucarana"
    start_date = date(2022, 2, 23)
