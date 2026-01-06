from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class PePetrolinaSpider(BaseDoemSpider):
    TERRITORY_ID = "2611101"
    name = "pe_petrolina"
    state_city_url_part = "pe/petrolina"
    start_date = date(2014, 3, 6)
