from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpCanitarSpider(DospGazetteSpider):
    TERRITORY_ID = "3510153"
    name = "sp_canitar"
    code = 4765
    start_date = date(2018, 9, 28)
