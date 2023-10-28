from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaMonteSantoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2921500"
    name = "ba_monte_santo"
    start_date = date(2021, 1, 2)
    state_city_url_part = "ba/montesanto"
