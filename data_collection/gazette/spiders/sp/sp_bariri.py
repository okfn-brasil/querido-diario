from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpBaririSpider(DospGazetteSpider):
    TERRITORY_ID = "3505203"
    name = "sp_bariri"
    code = 4707
    start_date = date(2017, 12, 13)
