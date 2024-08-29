from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsCandelariaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4304200"
    name = "rs_candelaria"
    city_subdomain = "candelaria"
    start_date = date(2019, 5, 7)
