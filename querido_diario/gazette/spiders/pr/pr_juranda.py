from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrJurandaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4112959"
    name = "pr_juranda"
    city_subdomain = "juranda"
    start_date = date(2021, 3, 24)
