from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMorungabaSpider(DospGazetteSpider):
    TERRITORY_ID = "3532009"
    name = "sp_morungaba"
    code = 5008
    start_date = date(2017, 8, 8)
