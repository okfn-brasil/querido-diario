from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class MgOliveiraSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "3145604"
    name = "mg_oliveira"
    city_subdomain = "oliveira"
    start_date = date(2014, 10, 22)
