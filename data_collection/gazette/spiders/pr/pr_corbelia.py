from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrCorbeliaSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4106308"
    name = "pr_corbelia"
    start_date = date(2015, 11, 20)  # Edição 1
    city_subdomain = "corbelia"
