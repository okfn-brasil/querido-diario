from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMirandopolisSpider(DospGazetteSpider):
    TERRITORY_ID = "3530102"
    name = "sp_mirandopolis"
    code = 4989
    start_date = date(2017, 7, 3)
