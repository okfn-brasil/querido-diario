from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrClevelandiaSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4105706"
    name = "pr_clevelandia"
    start_date = date(2012, 3, 26)  # Edição 60
    city_subdomain = "clevelandia"
