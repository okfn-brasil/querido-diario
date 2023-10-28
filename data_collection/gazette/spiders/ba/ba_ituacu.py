from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaItuacuSpider(DoemGazetteSpider):
    TERRITORY_ID = "2917201"
    name = "ba_ituacu"
    start_date = date(2018, 1, 2)
    state_city_url_part = "ba/ituacu"
