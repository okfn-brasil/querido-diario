from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class RsBentoGoncalvesSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4302105"
    name = "rs_bento_goncalves"
    start_date = date(2019, 4, 1)  # Edição 1124
    city_subdomain = "bentogoncalves"
