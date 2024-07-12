from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsBentoGoncalvesSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4302105"
    name = "rs_bento_goncalves"
    city_subdomain = "bentogoncalves"
    start_date = date(2019, 4, 1)
