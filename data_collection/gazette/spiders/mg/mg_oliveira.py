from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class MgOliveiraSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "3145604"
    name = "mg_oliveira"
    start_date = date(2014, 10, 22)  # Edição 1
    city_subdomain = "oliveira"
