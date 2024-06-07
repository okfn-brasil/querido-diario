from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpIbateSpider(DospGazetteSpider):
    TERRITORY_ID = "3519303"
    name = "sp_ibate"
    code = 4872
    start_date = date(2022, 11, 1)
