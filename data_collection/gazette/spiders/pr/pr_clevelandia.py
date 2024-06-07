from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrClevelandiaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4105706"
    name = "pr_clevelandia"
    city_subdomain = "clevelandia"
    start_date = date(2012, 3, 26)
