from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpIbiraremaSpider(DospGazetteSpider):
    TERRITORY_ID = "3519501"
    name = "sp_ibirarema"
    code = 4874
    start_date = date(2022, 5, 9)
