from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpGuaicaraSpider(DospGazetteSpider):
    TERRITORY_ID = "3517208"
    name = "sp_guaicara"
    code = 4847
    start_date = date(2017, 12, 12)
