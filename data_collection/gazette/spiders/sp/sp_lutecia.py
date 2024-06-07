from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpLuteciaSpider(DospGazetteSpider):
    TERRITORY_ID = "3527900"
    name = "sp_lutecia"
    code = 4965
    start_date = date(2018, 7, 30)
