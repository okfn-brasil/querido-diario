from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaAcajutibaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2900306"
    name = "ba_acajutiba"
    state_city_url_part = "ba/acajutiba"
    start_date = date(2013, 1, 30)
