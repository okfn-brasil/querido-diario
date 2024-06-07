from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpTarabaiSpider(DospGazetteSpider):
    TERRITORY_ID = "3553906"
    name = "sp_tarabai"
    code = 5252
    start_date = date(2018, 4, 9)
