from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpReginopolisSpider(DospGazetteSpider):
    TERRITORY_ID = "3542503"
    name = "sp_reginopolis"
    code = 5127
    start_date = date(2018, 2, 1)
