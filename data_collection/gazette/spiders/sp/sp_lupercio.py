from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpLupercioSpider(DospGazetteSpider):
    TERRITORY_ID = "3527801"
    name = "sp_lupercio"
    code = 4964
    start_date = date(2017, 6, 30)
