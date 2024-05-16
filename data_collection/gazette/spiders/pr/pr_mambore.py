from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrMamboreSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4114005"
    name = "pr_mambore"
    start_date = date(2020, 5, 25)  # Edição 1
    city_subdomain = "mambore"
