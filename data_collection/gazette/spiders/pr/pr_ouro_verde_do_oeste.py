from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrOuroVerdeDoOesteSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4117453"
    name = "pr_ouro_verde_do_oeste"
    start_date = date(2021, 3, 31)  # Edição 1
    city_subdomain = "ouroverdedooeste"
