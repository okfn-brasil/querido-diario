from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrGuaraniacuSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4109302"
    name = "pr_guaraniacu"
    start_date = date(2023, 5, 3)  # Edição 1
    city_subdomain = "guaraniacu"
