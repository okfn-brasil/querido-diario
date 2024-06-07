from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpItupevaSpider(DospGazetteSpider):
    TERRITORY_ID = "3524006"
    name = "sp_itupeva"
    code = 4924
    start_date = date(2019, 9, 24)
