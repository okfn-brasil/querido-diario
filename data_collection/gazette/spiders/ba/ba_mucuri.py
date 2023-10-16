from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaMucuriSpider(DoemGazetteSpider):
    TERRITORY_ID = "2922003"
    name = "ba_mucuri"
    start_date = date(2018, 1, 3)
    state_city_url_part = "ba/mucuri"
