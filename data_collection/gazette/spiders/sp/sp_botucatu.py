from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpBotucatuSpider(DospGazetteSpider):
    TERRITORY_ID = "3507506"
    name = "sp_botucatu"
    code = 4734
    start_date = date(2000, 1, 6)
