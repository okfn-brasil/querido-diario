from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrSantoAntonioDaPlatinaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4124103"
    name = "pr_santo_antonio_da_platina"
    city_subdomain = "santoantoniodaplatina"
    start_date = date(2024, 5, 16)
