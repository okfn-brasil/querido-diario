from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrApucaranaSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4101408"
    name = "pr_apucarana"
    start_date = date(2022, 2, 23)  # Edição 1
    city_subdomain = "apucarana"
