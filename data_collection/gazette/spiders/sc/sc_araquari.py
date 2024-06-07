from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class ScAraquariSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4201307"
    name = "sc_araquari"
    city_subdomain = "araquari"
    start_date = date(2018, 1, 2)
