from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpAnhembiSpider(DospGazetteSpider):
    TERRITORY_ID = "3502309"
    name = "sp_anhembi"
    code = 4674
    start_date = date(2024, 3, 12)
