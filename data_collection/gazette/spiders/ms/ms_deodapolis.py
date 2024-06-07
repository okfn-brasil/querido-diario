from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MsDeodapolisSpider(BaseDospSpider):
    TERRITORY_ID = "5003454"
    name = "ms_deodapolis"
    code = 1492
    start_date = date(2023, 11, 17)
