from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaCristopolisSpider(DoemGazetteSpider):
    TERRITORY_ID = "2909703"
    name = "ba_cristopolis"
    state_city_url_part = "ba/cristopolis"
    start_date = date(2021, 1, 12)
