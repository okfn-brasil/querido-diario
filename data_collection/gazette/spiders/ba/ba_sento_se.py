from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaSentoSeSpider(DoemGazetteSpider):
    TERRITORY_ID = "2930204"
    name = "ba_sento_se"
    state_city_url_part = "ba/sentose"
    start_date = date(2017, 1, 2)
