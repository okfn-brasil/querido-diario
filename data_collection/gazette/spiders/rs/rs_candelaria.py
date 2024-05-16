from datetime import date

from gazette.spiders.base.atende_layoutdois import BaseAtendeL2Spider


class RsCandelariaSpider(BaseAtendeL2Spider):
    TERRITORY_ID = "4304200"
    name = "rs_candelaria"
    start_date = date(2023, 5, 7)  # Edição 1
    city_subdomain = "candelaria"
