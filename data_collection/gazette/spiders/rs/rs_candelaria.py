from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class RsCandelariaSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4304200"
    name = "rs_candelaria"
    start_date = date(2023, 5, 7)  # Edição 1
    city_subdomain = "candelaria"
