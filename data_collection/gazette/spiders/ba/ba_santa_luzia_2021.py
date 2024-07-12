from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaSantaLuziaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2928059"
    name = "ba_santa_luzia_2021"
    state_city_url_part = "ba/santaluzia"
    start_date = date(2021, 1, 4)
    end_date = date(2024, 1, 29)
