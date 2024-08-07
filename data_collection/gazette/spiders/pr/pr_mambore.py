from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrMamboreSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4114005"
    name = "pr_mambore"
    city_subdomain = "mambore"
    start_date = date(2020, 5, 25)
