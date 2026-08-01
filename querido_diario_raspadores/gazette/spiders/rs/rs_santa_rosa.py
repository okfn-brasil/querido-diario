from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsSantaRosaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4317202"
    name = "rs_santa_rosa"
    city_subdomain = "santarosa"
    start_date = date(2022, 8, 23)
