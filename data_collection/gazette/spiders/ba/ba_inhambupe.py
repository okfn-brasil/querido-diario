from gazette.spiders.base.doem import DoemGazetteSpider
from datetime import date


class BaInhambupeSpider(DoemGazetteSpider):
    TERRITORY_ID = "2913705"
    name = "ba_inhambupe"
    start_date = date(2018, 1, 2)
    state_city_url_part = "ba/inhambupe"
