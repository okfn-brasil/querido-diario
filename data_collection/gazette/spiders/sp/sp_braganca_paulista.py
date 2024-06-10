from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpBragancaPaulistaSpider(DospGazetteSpider):
    TERRITORY_ID = "3507605"
    name = "sp_braganca_paulista"
    code = 4735
    start_date = date(2019, 1, 4)
