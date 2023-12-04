from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrTupassiSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4127957"
    name = "pr_tupassi"
    start_date = date(2016, 6, 27)  # Edição 14
    city_subdomain = "tupassi"
