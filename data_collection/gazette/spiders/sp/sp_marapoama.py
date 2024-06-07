from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMarapoamaSpider(DospGazetteSpider):
    TERRITORY_ID = "3528858"
    name = "sp_marapoama"
    code = 4975
    start_date = date(2024, 2, 2)
