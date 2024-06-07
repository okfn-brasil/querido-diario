from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpDobradaSpider(DospGazetteSpider):
    TERRITORY_ID = "3514007"
    name = "sp_dobrada"
    code = 4805
    start_date = date(2016, 6, 3)
