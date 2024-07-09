from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaCipoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2907905"
    name = "ba_cipo"
    state_city_url_part = "ba/cipo"
    start_date = date(2021, 1, 4)
