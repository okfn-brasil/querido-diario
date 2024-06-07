from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpNovaisSpider(DospGazetteSpider):
    TERRITORY_ID = "3533254"
    name = "sp_novais"
    code = 5028
    start_date = date(2023, 1, 16)
