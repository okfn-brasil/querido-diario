from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMiguelopolisSpider(DospGazetteSpider):
    TERRITORY_ID = "3529708"
    name = "sp_miguelopolis"
    code = 4985
    start_date = date(2024, 5, 2)
