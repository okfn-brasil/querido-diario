from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class RsGravataiSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4309209"
    name = "rs_gravatai"
    start_date = date(2015, 5, 4)  # Edição 1
    city_subdomain = "gravatai"
    power = "executive"
