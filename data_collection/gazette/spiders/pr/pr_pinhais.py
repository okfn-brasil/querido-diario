from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrPinhaisSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4119152"
    name = "pr_pinhais"
    start_date = date(2017, 5, 26)  # Edição 1
    city_subdomain = "pinhais"
