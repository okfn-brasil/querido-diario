from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpBiriguiSpider(DospGazetteSpider):
    TERRITORY_ID = "3506508"
    name = "sp_birigui"
    code = 4722
    start_date = date(2016, 12, 28)
