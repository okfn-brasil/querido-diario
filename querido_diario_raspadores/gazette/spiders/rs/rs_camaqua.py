from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsCamaquaSpider(BaseAtendeV2Spider):
    name = "rs_camaqua"
    TERRITORY_ID = "4303509"
    city_subdomain = "camaqua"
    start_date = date(2019, 7, 25)
