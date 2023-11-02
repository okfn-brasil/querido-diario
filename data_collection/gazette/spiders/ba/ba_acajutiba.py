from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaAcajutibaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2900306"
    name = "ba_acajutiba"
    start_date = date(2018, 1, 2)
    state_city_url_part = "ba/acajutiba"
