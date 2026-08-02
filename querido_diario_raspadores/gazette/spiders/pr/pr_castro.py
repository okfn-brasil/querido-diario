from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrCastroSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4104907"
    name = "pr_castro"
    city_subdomain = "castro"
    start_date = date(2010, 6, 4)
