from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpTaiuvaSpider(DospGazetteSpider):
    TERRITORY_ID = "3553203"
    name = "sp_taiuva"
    code = 5243
    start_date = date(2017, 12, 18)
