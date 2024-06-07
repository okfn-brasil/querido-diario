from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpUruSpider(DospGazetteSpider):
    TERRITORY_ID = "3555901"
    name = "sp_uru"
    code = 5277
    start_date = date(2018, 7, 12)
