from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpBalsamoSpider(DospGazetteSpider):
    TERRITORY_ID = "3504800"
    name = "sp_balsamo"
    code = 4703
    start_date = date(2017, 2, 22)
