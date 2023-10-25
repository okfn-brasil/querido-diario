from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaMorroDoChapeuSpider(DoemGazetteSpider):
    TERRITORY_ID = "2921708"
    name = "ba_morro_do_chapeu"
    start_date = date(2021, 1, 6)
    state_city_url_part = "ba/morrodochapeu"
