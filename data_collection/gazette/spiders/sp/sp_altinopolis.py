from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpAltinopolisSpider(DospGazetteSpider):
    TERRITORY_ID = "3501004"
    name = "sp_altinopolis"
    code = 4660
    start_date = date(2017, 9, 4)
