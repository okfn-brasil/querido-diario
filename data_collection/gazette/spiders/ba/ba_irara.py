from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaIraraSpider(DoemGazetteSpider):
    TERRITORY_ID = "2914505"
    name = "ba_irara"
    state_city_url_part = "ba/irara"
    start_date = date(2014, 4, 24)
