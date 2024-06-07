from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpClementinaSpider(DospGazetteSpider):
    TERRITORY_ID = "3511904"
    name = "sp_clementina"
    code = 4783
    start_date = date(2022, 10, 26)
