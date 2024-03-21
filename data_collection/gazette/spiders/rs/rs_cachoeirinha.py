from datetime import date

from gazette.spiders.base.atende import BaseAtendeT1Spider


class RsCachoeirinhaSpider(BaseAtendeT1Spider):
    TERRITORY_ID = "4303103"
    name = "rs_cachoeirinha"
    start_date = date(2013, 5, 15)  # Edição 1
    city_subdomain = "cachoeirinha"
    perm_url = "diario-oficial-de-cachoeirinha"
