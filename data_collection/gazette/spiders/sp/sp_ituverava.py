from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpItuveravaSpider(DospGazetteSpider):
    TERRITORY_ID = "3524105"
    name = "sp_ituverava"
    code = 4925
    start_date = date(2022, 12, 8)
