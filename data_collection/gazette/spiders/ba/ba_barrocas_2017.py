from gazette.spiders.base.doem import DoemGazetteSpider
from datetime import date

class BaBarrocasSpider(DoemGazetteSpider):
    TERRITORY_ID = "2903276"
    name = "ba_barrocas_2017"
    state_city_url_part = "ba/barrocas"
    start_date = date(2017, 1, 2)
