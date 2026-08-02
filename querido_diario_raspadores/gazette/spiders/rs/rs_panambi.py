from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsPanambiSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4313904"
    name = "rs_panambi"
    city_subdomain = "panambi"
    start_date = date(2021, 4, 14)
