from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrPatoBragadoSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4118451"
    name = "pr_pato_bragado"
    start_date = date(2012, 5, 30)  # Edição 1
    city_subdomain = "patobragado"
