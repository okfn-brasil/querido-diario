from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class RsDoisIrmaosSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4306403"
    name = "rs_dois_irmaos"
    city_subdomain = "doisirmaos"
    start_date = date(2020, 1, 7)
