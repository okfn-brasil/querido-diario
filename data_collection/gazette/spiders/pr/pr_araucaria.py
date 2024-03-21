from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrCampoMouraoSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4101804"
    name = "pr_araucaria"
    start_date = date(2018, 12, 19)  # Edição 246
    city_subdomain = "araucaria"
