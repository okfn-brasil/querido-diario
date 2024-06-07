from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpIpuaSpider(DospGazetteSpider):
    TERRITORY_ID = "3521309"
    name = "sp_ipua"
    code = 4895
    start_date = date(2019, 12, 12)
