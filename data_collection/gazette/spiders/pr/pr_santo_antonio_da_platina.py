from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrSantoAntonioDaPlatinaSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4124103"
    name = "pr_santo_antonio_da_platina"
    start_date = date(2012, 11, 27)  # Edição 1
    city_subdomain = "santoantoniodaplatina"
