from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpIgarapavaSpider(DospGazetteSpider):
    TERRITORY_ID = "3520103"
    name = "sp_igarapava"
    code = 4880
    start_date = date(2019, 10, 10)
