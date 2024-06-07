from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpPederneirasSpider(DospGazetteSpider):
    TERRITORY_ID = "3536703"
    name = "sp_pederneiras"
    code = 5064
    start_date = date(2018, 1, 15)
