from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpTanabiSpider(DospGazetteSpider):
    TERRITORY_ID = "3553401"
    name = "sp_tanabi"
    code = 5245
    start_date = date(2019, 6, 17)
