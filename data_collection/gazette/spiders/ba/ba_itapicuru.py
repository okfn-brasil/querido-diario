from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaItapicuruSpider(DoemGazetteSpider):
    TERRITORY_ID = "2916500"
    name = "ba_itapicuru"
    start_date = date(2021, 1, 4)
    state_city_url_part = "ba/itapicuru"
