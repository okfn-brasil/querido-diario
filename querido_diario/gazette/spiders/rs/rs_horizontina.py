from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsHorizontinaSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4309605"
    name = "rs_horizontina"
    city_subdomain = "horizontina"
    start_date = date(2016, 6, 15)
