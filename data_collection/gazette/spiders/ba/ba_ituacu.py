from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaItuacuSpider(DoemGazetteSpider):
    TERRITORY_ID = "2917201"
    name = "ba_ituacu"
    state_city_url_part = "ba/ituacu"
    start_date = date(2015, 2, 4)
