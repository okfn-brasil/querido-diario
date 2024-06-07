from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpDolcinopolisSpider(DospGazetteSpider):
    TERRITORY_ID = "3514205"
    name = "sp_dolcinopolis"
    code = 4807
    start_date = date(2018, 1, 15)
