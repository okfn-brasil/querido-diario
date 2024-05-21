from datetime import date

from gazette.spiders.base.atende_layoutdois import BaseAtendeL2Spider


class RsBentoGoncalvesSpider(BaseAtendeL2Spider):
    TERRITORY_ID = "4302105"
    name = "rs_bento_goncalves"
    start_date = date(2019, 4, 1)  # Edição 1124
    city_subdomain = "bentogoncalves"
    # power
