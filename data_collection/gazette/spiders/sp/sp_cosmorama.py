from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpCosmoramaSpider(DospGazetteSpider):
    TERRITORY_ID = "3512902"
    name = "sp_cosmorama"
    code = 4793
    start_date = date(2015, 4, 9)
