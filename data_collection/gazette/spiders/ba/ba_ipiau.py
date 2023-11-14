from gazette.spiders.base.doem import DoemGazetteSpider
from  datetime import date


class BaIpiauSpider(DoemGazetteSpider):
    TERRITORY_ID = "2913903"
    name = ""
    start_date = date(2018, 1, 2)
    state_city_url_part = "ba/ipiau"
