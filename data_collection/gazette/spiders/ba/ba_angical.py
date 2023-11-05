from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaAngicalSpider(DoemGazetteSpider):
    TERRITORY_ID = "2901403"
    name = "ba_angical"
    start_date = date(2021, 1, 4)
    state_city_url_part = "ba/angical"