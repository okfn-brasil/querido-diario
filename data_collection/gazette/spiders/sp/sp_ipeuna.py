from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpIpeunaSpider(DospGazetteSpider):
    TERRITORY_ID = "3521101"
    name = "sp_ipeuna"
    code = 4892
    start_date = date(2019, 10, 15)
