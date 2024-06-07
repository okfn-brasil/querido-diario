from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMotucaSpider(DospGazetteSpider):
    TERRITORY_ID = "3532058"
    name = "sp_motuca"
    code = 5009
    start_date = date(2024, 4, 11)
