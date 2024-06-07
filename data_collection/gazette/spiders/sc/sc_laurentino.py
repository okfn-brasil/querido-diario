from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class ScLaurentinoSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4209508"
    name = "sc_laurentino"
    city_subdomain = "laurentino"
    start_date = date(2021, 7, 1)
