from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpJumirimSpider(DospGazetteSpider):
    TERRITORY_ID = "3525854"
    name = "sp_jumirim"
    code = 4943
    start_date = date(2017, 12, 8)
