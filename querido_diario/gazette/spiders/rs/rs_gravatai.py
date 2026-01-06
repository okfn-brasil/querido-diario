from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsGravataiSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4309209"
    name = "rs_gravatai"
    city_subdomain = "gravatai"
    start_date = date(2015, 5, 4)
