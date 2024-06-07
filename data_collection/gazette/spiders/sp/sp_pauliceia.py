from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpPauliceiaSpider(DospGazetteSpider):
    TERRITORY_ID = "3536406"
    name = "sp_pauliceia"
    code = 5060
    start_date = date(2019, 3, 19)
