from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsGramadoSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4309100"
    name = "rs_gramado"
    city_subdomain = "gramado"
    start_date = date(2022, 1, 4)
