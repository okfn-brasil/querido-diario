from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMartinopolisSpider(DospGazetteSpider):
    TERRITORY_ID = "3529203"
    name = "sp_martinopolis"
    code = 4979
    start_date = date(2018, 7, 5)
