from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class MgCarmopolisDeMinasSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "3114501"
    name = "mg_carmopolis_de_minas"
    start_date = date(2013, 1, 24)  # Edição 64
    city_subdomain = "carmopolisdeminas"
