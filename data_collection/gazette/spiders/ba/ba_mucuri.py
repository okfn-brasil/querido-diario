from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaMucuriSpider(DoemGazetteSpider):
    TERRITORY_ID = "2922003"
    name = "ba_mucuri"
    state_city_url_part = "ba/mucuri"
    start_date = date(2011, 4, 5)
