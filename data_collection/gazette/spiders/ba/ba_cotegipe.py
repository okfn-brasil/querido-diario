from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaCotegipeSpider(DoemGazetteSpider):
    TERRITORY_ID = "2909406"
    name = "ba_cotegipe"
    state_city_url_part = "ba/cotegipe"
    start_date = date(2023, 1, 5)
