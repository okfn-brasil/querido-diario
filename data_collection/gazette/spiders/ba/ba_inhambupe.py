from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaInhambupeSpider(DoemGazetteSpider):
    TERRITORY_ID = "2913705"
    name = "ba_inhambupe"
    state_city_url_part = "ba/inhambupe"
    start_date = date(2013, 1, 2)
