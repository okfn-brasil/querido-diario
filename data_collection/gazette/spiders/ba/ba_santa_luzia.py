from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaSantaLuziaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2928059"
    name = "ba_santa_luzia"
    start_date = date(2021, 1, 4)
    state_city_url_part = "ba/santaluzia"
