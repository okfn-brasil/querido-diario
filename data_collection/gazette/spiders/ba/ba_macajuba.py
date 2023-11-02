from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaMacajubaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2919603"
    name = "ba_macajuba"
    start_date = date(2014, 3, 17)
    state_city_url_part = "ba/macajuba"
