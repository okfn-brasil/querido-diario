from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpCoroadosSpider(DospGazetteSpider):
    TERRITORY_ID = "3512506"
    name = "sp_coroados"
    code = 4789
    start_date = date(2018, 2, 16)
