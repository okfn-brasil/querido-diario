from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpPongaiSpider(DospGazetteSpider):
    TERRITORY_ID = "3540101"
    name = "sp_pongai"
    code = 5098
    start_date = date(2018, 8, 2)
