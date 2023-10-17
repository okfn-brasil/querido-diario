from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaCaculeSpider(DoemGazetteSpider):
    TERRITORY_ID = "2905008"
    name = "ba_cacule_2015"
    state_city_url_part = "ba/cacule"
    start_date = date(2015, 1, 2)
