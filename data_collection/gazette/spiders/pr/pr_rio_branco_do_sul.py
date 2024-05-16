from datetime import date

from gazette.spiders.base.atende import BaseAtendeT2Spider


class PrRioBrancoDoSulSpider(BaseAtendeT2Spider):
    TERRITORY_ID = "4122206"
    name = "pr_rio_branco_do_sul"
    start_date = date(2022, 11, 20)  # Edição 2608
    city_subdomain = "riobrancodosul"
