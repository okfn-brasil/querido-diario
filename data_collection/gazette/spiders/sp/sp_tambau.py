from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpTambauSpider(DospGazetteSpider):
    TERRITORY_ID = "3553302"
    name = "sp_tambau"
    code = 5244
    start_date = date(2019, 11, 26)
