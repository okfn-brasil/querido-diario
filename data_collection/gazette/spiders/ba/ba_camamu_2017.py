from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaCamamuSpider(DoemGazetteSpider):
    TERRITORY_ID = "2905800"
    name = "ba_camamu_2017"
    state_city_url_part = "ba/camamu"
    start_date = date(2017, 1, 3)
