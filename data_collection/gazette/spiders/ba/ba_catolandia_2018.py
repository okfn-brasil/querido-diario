from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaCatolandiaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2907400"
    name = "ba_catolandia_2018"
    state_city_url_part = "ba/catolandia"
    start_date = date(2018, 1, 29)
