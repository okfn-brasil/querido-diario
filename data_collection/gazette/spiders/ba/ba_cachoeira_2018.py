from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaCachoeiraSpider(DoemGazetteSpider):
    TERRITORY_ID = "2904902"
    name = "ba_cachoeira_2018"
    state_city_url_part = "ba/cachoeira"
    start_date = date(2018, 1, 9)
