from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaSatiroDiasSpider(DoemGazetteSpider):
    TERRITORY_ID = "2929701"
    name = "ba_satiro_dias"
    start_date = date(2021, 3, 30)
    state_city_url_part = "ba/satirodias"
