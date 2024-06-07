from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpRifainaSpider(DospGazetteSpider):
    TERRITORY_ID = "3543600"
    name = "sp_rifaina"
    code = 5139
    start_date = date(2024, 4, 2)
