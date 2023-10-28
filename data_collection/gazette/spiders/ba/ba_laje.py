from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaLajeSpider(DoemGazetteSpider):
    TERRITORY_ID = "2918902"
    name = "ba_laje"
    start_date = date(2020, 1, 8)
    state_city_url_part = "ba/laje"
