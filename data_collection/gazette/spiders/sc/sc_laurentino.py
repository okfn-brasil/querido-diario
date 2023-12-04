from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class ScLaurentinoSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4209508"
    name = "sc_laurentino"
    start_date = date(2021, 7, 1)  # Edição 1
    city_subdomain = "laurentino"
