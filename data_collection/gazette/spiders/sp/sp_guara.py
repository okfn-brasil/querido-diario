from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpGuaraSpider(DospGazetteSpider):
    TERRITORY_ID = "3517703"
    name = "sp_guara"
    code = 4852
    start_date = date(2014, 12, 12)
