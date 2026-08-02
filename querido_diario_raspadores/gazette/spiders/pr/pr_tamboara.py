from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class PrTamboaraSpider(BaseDoemSpider):
    TERRITORY_ID = "4126702"
    name = "pr_tamboara"
    state_city_url_part = "pr/tamboara"
    start_date = date(2022, 8, 22)
