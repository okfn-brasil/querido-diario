from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class MsRioBrilhanteSpider(DospGazetteSpider):
    TERRITORY_ID = "5007208"
    name = "ms_rio_brilhante"
    code = 1526
    start_date = date(2024, 2, 1)
