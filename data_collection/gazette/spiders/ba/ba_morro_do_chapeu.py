from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaMorroDoChapeuSpider(DoemGazetteSpider):
    TERRITORY_ID = "2921708"
    name = "ba_morro_do_chapeu"
    state_city_url_part = "ba/morrodochapeu"
    start_date = date(2013, 3, 1)
