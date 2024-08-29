from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaAngicalSpider(DoemGazetteSpider):
    TERRITORY_ID = "2901403"
    name = "ba_angical"
    state_city_url_part = "ba/angical"
    start_date = date(2021, 1, 4)
