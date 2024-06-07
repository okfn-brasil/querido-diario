from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class MgCarmopolisDeMinasSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "3114501"
    name = "mg_carmopolis_de_minas"
    city_subdomain = "carmopolisdeminas"
    start_date = date(2013, 1, 24)
