from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaIraraSpider(DoemGazetteSpider):
    TERRITORY_ID = "2914505"
    name = "ba_irara"
    start_date = date(2018, 1, 3)
    state_city_url_part = "ba/irara"
