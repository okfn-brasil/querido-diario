from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaCatuSpider(DoemGazetteSpider):
    TERRITORY_ID = "2907509"
    name = "ba_catu_2014"
    state_city_url_part = "ba/catu"
    start_date = date(2014, 7, 17)
