from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpViradouroSpider(DospGazetteSpider):
    TERRITORY_ID = "3556800"
    name = "sp_viradouro"
    code = 5288
    start_date = date(2013, 6, 5)
