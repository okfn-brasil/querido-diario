from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpTuiutiSpider(DospGazetteSpider):
    TERRITORY_ID = "3554953"
    name = "sp_tuiuti"
    code = 5266
    start_date = date(2014, 10, 9)
