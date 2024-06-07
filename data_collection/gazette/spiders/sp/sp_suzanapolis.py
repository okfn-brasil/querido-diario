from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSuzanapolisSpider(DospGazetteSpider):
    TERRITORY_ID = "3552551"
    name = "sp_suzanapolis"
    code = 5235
    start_date = date(2018, 9, 27)
