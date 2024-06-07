from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpBrodowskiSpider(DospGazetteSpider):
    TERRITORY_ID = "3507803"
    name = "sp_brodowski"
    code = 4738
    start_date = date(2017, 8, 8)
