from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class RsHorizontinaSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4309605"
    name = "rs_horizontina"
    start_date = date(2016, 6, 15)  # Edição 1
    city_subdomain = "horizontina"
