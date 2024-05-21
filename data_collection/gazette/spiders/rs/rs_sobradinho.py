from datetime import date

from gazette.spiders.base.atende_layoutdois import BaseAtendeL2Spider


class RsSobradinhoSpider(BaseAtendeL2Spider):
    TERRITORY_ID = "4320701"
    name = "rs_sobradinho"
    start_date = date(2020, 3, 5)  # Edição 1
    city_subdomain = "sobradinho"
