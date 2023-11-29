from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class RsPanambiSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4313904"
    name = "rs_panambi"
    start_date = date(2021, 4, 14)  # Edição 1
    city_subdomain = "panambi"
