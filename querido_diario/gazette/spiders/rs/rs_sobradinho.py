from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsSobradinhoSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4320701"
    name = "rs_sobradinho"
    city_subdomain = "sobradinho"
    start_date = date(2020, 3, 5)
