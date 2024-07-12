from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpTremembeSpider(DospGazetteSpider):
    TERRITORY_ID = "3554805"
    name = "sp_tremembe"
    code = 5264
    start_date = date(2016, 5, 11)
