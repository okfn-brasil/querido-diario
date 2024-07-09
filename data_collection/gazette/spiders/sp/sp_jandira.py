from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpJandiraSpider(DospGazetteSpider):
    TERRITORY_ID = "3525003"
    name = "sp_jandira"
    code = 4934
    start_date = date(2022, 3, 22)
