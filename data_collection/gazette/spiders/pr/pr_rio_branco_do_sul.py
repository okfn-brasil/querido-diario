from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrRioBrancoDoSulSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4122206"
    name = "pr_rio_branco_do_sul"
    city_subdomain = "riobrancodosul"
    start_date = date(2022, 9, 20)
