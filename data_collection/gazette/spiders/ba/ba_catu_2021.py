from gazette.spiders.base.doem import DoemGazetteSpider
from datetime import date

class BaCatuSpider(DoemGazetteSpider):
    TERRITORY_ID = "2907509"
    name = "ba_catu_2021"
    start_date = date(2014, 7, 17)
    state_city_url_part = "ba/catu"
