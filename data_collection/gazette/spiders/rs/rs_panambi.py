from datetime import date

from gazette.spiders.base.atende_layoutdois import BaseAtendeL2Spider


class RsPanambiSpider(BaseAtendeL2Spider):
    TERRITORY_ID = "4313904"
    name = "rs_panambi"
    start_date = date(2021, 4, 14)  # Edição 1
    city_subdomain = "panambi"
