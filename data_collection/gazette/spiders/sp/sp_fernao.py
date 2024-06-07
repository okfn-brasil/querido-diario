from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpFernaoSpider(DospGazetteSpider):
    TERRITORY_ID = "3515657"
    name = "sp_fernao"
    code = 4830
    start_date = date(2018, 2, 1)
