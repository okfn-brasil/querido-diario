from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrPatoBragadoSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4118451"
    name = "pr_pato_bragado"
    city_subdomain = "patobragado"
    start_date = date(2012, 5, 30)
