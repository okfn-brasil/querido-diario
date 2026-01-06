from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrCorbeliaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4106308"
    name = "pr_corbelia"
    city_subdomain = "corbelia"
    start_date = date(2015, 11, 20)
