from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrJurandaSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4112959"
    name = "pr_juranda"
    start_date = date(2021, 3, 24)  # Edição 1
    city_subdomain = "juranda"
