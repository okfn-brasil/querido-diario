from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpDirceReisSpider(DospGazetteSpider):
    TERRITORY_ID = "3513850"
    name = "sp_dirce_reis"
    code = 4803
    start_date = date(2019, 4, 4)
